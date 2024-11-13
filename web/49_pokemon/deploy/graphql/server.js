var express = require("express");
var { createHandler } = require("graphql-http/lib/use/express");
var { buildSchema } = require("graphql");
var { readFileSync } = require("fs");
const argv = require("minimist")(process.argv.slice(2));
const db = require("better-sqlite3")("database.db");

console.log("Loading GraphQL schema...");
var schema = buildSchema(readFileSync(__dirname + "/schema.graphql", "utf8"))
console.log("GraphQL schema loading completed!")

// The root provides a resolver function for each API endpoint
var root = {
    hello() {
        return "Hello world!"
    },
    bye() {
        return "Goodbye world!"
    },
    pokemon(args) {
        const res = db.prepare("SELECT * FROM pokemons WHERE name = ?").get(args.name);
        return res;
    },
    digimOwOUwURawrn38408375018458385023841203489738570123(args) {
        if (args.passcode === process.env.PASSCODE) {
            const res = db.prepare("SELECT * FROM digimons WHERE name = ?").get(args.name);
            return res;
        }
        return null;
    }
}

const WORKER_COUNT = parseInt(argv["w"]);
var servers = [];
for (var i = 0; i < WORKER_COUNT; i++) {
    let app = express();
    app.use(express.json());

    // health endpoint
    app.get("/health", (req, res) => {
        res.send("OK");
    });

    // GraphQL endpoint
    app.all(
        "/graphql",
        createHandler({
            schema: schema,
            rootValue: root,
        })
    )
    servers.push(app);
}

for (var i = 0; i < WORKER_COUNT; i++) {
    servers[i].listen(4001 + i);
    console.log(`Running GraphQL API server with port ${4001 + i}...`);
}