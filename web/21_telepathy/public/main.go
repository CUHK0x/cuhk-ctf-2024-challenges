package main

import (
	"database/sql"
	"encoding/json"
	"fmt"
	"io"
	"net"
	"net/http"
	"os"
	"regexp"
	"strings"
	"sync"
	"time"

	"golang.org/x/time/rate"

	_ "github.com/lib/pq"
)

// database
var db *sql.DB

type Item struct {
	Name        string `json:"name"`
	Description string `json:"description"`
}

type Items struct {
	Items []Item `json:"items"`
}

// rate limiter
type visitor struct {
	limiter  *rate.Limiter
	lastSeen time.Time
}

var visitors = make(map[string]*visitor)
var mu sync.Mutex

// Run a background goroutine to remove old entries from the visitors map.
func initBackground() {
	go cleanupVisitors()
}

func cleanupVisitors() {
	for {
		time.Sleep(time.Minute)

		mu.Lock()
		for ip, v := range visitors {
			if time.Since(v.lastSeen) > 3*time.Minute {
				delete(visitors, ip)
			}
		}
		mu.Unlock()
	}
}

func getVisitor(ip string) *rate.Limiter {
	mu.Lock()
	defer mu.Unlock()

	vstr, exists := visitors[ip]
	if !exists {
		limiter := rate.NewLimiter(1, 10) // refills token every 2 second, maximum 10 tokens
		visitors[ip] = &visitor{limiter, time.Now()}
		vstr = visitors[ip]
	}

	vstr.lastSeen = time.Now()

	return vstr.limiter
}

func limit(next http.HandlerFunc) http.HandlerFunc {
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		ip, _, err := net.SplitHostPort(r.RemoteAddr)
		if err != nil {
			http.Error(w, "Internal Server Error", http.StatusInternalServerError)
			return
		}

		limiter := getVisitor(ip)
		if !limiter.Allow() {
			http.Error(w, http.StatusText(429), http.StatusTooManyRequests)
			return
		}

		next.ServeHTTP(w, r)
	})
}

// constant variables
var (
	postgresUser     = os.Getenv("POSTGRES_USER")
	postgresPassword = os.Getenv("POSTGRES_PASSWORD")
	readonlyUser     = "ctfuser"
	readonlyPassword = os.Getenv("POSTGRES_READONLY_PASSWORD")
	dbName           = "postgres"
	bannedCharacters = `[^a-zA-Z0-9{\\'"_\-$ }]`
	bannedWords      = `(?i)like|similar +to`
)

// initialise the database
func initDB() {
	var err error

	flagFile, err := os.Open("flag.txt")
	if err != nil {
		panic(err)
	}
	defer flagFile.Close()

	flag, _ := io.ReadAll(flagFile)

	connStr := fmt.Sprintf("host=%s port=%d user=%s password=%s dbname=%s sslmode=disable", "telepathy-db", 5432, postgresUser, postgresPassword, dbName)
	rootDB, err := sql.Open("postgres", connStr)
	if err != nil {
		panic(err)
	}
	defer rootDB.Close()

	createTableStmt := `
        DROP TABLE IF EXISTS items;
        CREATE TABLE IF NOT EXISTS items (
            id INT NOT NULL GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
            name TEXT,
            description TEXT
        )
    `

	createUserStmt := fmt.Sprintf(`
        DROP USER IF EXISTS %s;
        DO $$
        BEGIN
            IF EXISTS (SELECT FROM pg_catalog.pg_roles WHERE rolname = 'read_only') THEN
                DROP OWNED BY read_only;
                DROP ROLE read_only;
            END IF;
        END;
        $$;
        CREATE ROLE read_only;
        GRANT CONNECT ON DATABASE postgres TO read_only;
        GRANT USAGE ON SCHEMA public TO read_only;
        GRANT SELECT ON ALL TABLES IN SCHEMA public TO read_only;
        CREATE USER %s WITH PASSWORD '%s';
        GRANT read_only TO %s;
    `, readonlyUser, readonlyUser, readonlyPassword, readonlyUser)

	_, err = rootDB.Exec(createTableStmt)
	if err != nil {
		panic(err)
	}

	_, err = rootDB.Exec(createUserStmt)
	if err != nil {
		panic(err)
	}

	var count int

	err = rootDB.QueryRow("SELECT COUNT(*) FROM items").Scan(&count)
	if err != nil {
		panic(err)
	}

	if count == 0 {
		jsonFile, err := os.Open("items.json")
		if err != nil {
			panic(err)
		}
		defer jsonFile.Close()

		bytes, _ := io.ReadAll(jsonFile)

		var items Items
		json.Unmarshal(bytes, &items)
		for _, item := range items.Items {
			insertStmt := fmt.Sprintf(`INSERT INTO items (name, description) VALUES (E'%s', E'%s')`, item.Name, item.Description)
			_, err = rootDB.Exec(insertStmt)
			if err != nil {
				panic(err)
			}
		}
		flagInsertStmt := fmt.Sprintf(`INSERT INTO items (name, description) VALUES ('Flagmon', 'Flagmon stores a flag called %s')`, string(flag))
		_, err = rootDB.Exec(flagInsertStmt)
		if err != nil {
			panic(err)
		}
	}
}

// get the readonly SQL connection
func getReadonlyDB() *sql.DB {
	var err error

	if db == nil {
		connStr := fmt.Sprintf("host=%s port=%d user=%s password=%s dbname=%s sslmode=disable", "telepathy-db", 5432, readonlyUser, readonlyPassword, dbName)
		db, err = sql.Open("postgres", connStr)
		if err != nil {
			panic(err)
		}
	}

	return db
}

// ready to test in production
func postQuery(w http.ResponseWriter, r *http.Request) {
	if r.Method == http.MethodPost {
		r.ParseForm()
		value := r.Form.Get("value")

		re := regexp.MustCompile(bannedCharacters)
		re2 := regexp.MustCompile(bannedWords)
		if re.MatchString(value) || re2.MatchString(value) {
			w.WriteHeader(http.StatusTeapot)
			fmt.Fprintln(w, "WIP")
			return
		}

		value = strings.ReplaceAll(value, `'`, `\'`)

		db := getReadonlyDB()
		preparedStmt := fmt.Sprintf(`SELECT * FROM items WHERE name = E'%s'`, value)
		_, err := db.Exec(preparedStmt)

		if err != nil {
			w.WriteHeader(http.StatusBadRequest)
			fmt.Fprintln(w, err)
			return
		}

		// TODO: return YES/NO (tomorrow do, it's 5am already for me...)
		fmt.Fprintln(w, "WIP")
		return
	}
	w.WriteHeader(http.StatusMethodNotAllowed)
	fmt.Fprintln(w, "Method not allowed")
}

func main() {
	go initDB()
	go initBackground()

	mux := http.NewServeMux()
	mux.Handle("/", http.FileServer(http.Dir("./static"))) // no rate limit required
	mux.HandleFunc("/query", limit(postQuery))

	fmt.Println("Go webserver serving at port 8080")
	http.ListenAndServe(":8080", mux)
}
