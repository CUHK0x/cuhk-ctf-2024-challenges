from flask import Flask, request, send_file
import requests, json, os, re, time

app = Flask(__name__)

last_time_fetch = 0

@app.route("/api/health")
def index():
    return { "status" : "OK" }

@app.route("/api/query", methods=['POST'])
def query():
    data = request.get_json()
    pokemons = data["pokemons"]
    compares = data["compares"]
    compares_string = ' '.join(compares)
    pokemon_template = '_{num}:pokemon(name:"{pokemon}"){{{compares}}}'
    query_string = "{{{query}}}"
    query = []
    for pokemon, index in zip(pokemons, range(1, len(pokemons) + 1)):
        curr = pokemon_template.format(num=index, pokemon=pokemon, compares=compares_string)
        query.append(curr)
    final_query = query_string.format(query=','.join(query))
    returned_data = json.loads(requests.get("http://pokemon-graphql:4000/graphql?query="+final_query).text)
    if returned_data.get('data') is None:
        returned_data["errors"] = "Error found while querying!"
        returned_data["query"] = final_query
    return returned_data

@app.route("/api/image", methods=['GET'])
def image():
    global last_time_fetch
    id = request.args.get('id')
    if re.fullmatch(r"^\d{3,4}$", id) and 1 <= int(id) and int(id) <= 1025:
        path = os.path.join(os.getcwd(), 'images', f"{id}.png")
        if not os.path.isfile(path):
            # rate limit
            wait_time = max(0, last_time_fetch + 5 - time.time())
            time.sleep(wait_time)
            last_time_fetch = time.time()
            r = requests.get(f"https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/{id}.png")
            if r.status_code != 200 or r.content[:4] != b"\x89\x50\x4E\x47":
                return "Cannot fetch image", 404
            else:
                if not os.path.exists("images"):
                    os.mkdir("images")
                with open(f"images/{id}.png", "wb") as f:
                    f.write(r.content)
                    f.flush()
        return send_file(path, mimetype='image/png')
    return "Invalid ID", 400
        