import random
import sys

random.seed(' '.join(sys.argv))

template = """
type Pokemon {{
    id: Int!,
    name: String!,
    type1: String!,
    type2: String,
    abilities: String!,
    hp: Int!,
    attack: Int!,
    defense: Int!,
    spattack: Int!,
    spdefense: Int!,
    speed: Int!
}}

{digimons}

type Query {{
    hello: String
    bye: String
    pokemon(name: String!): Pokemon
    digimOwOUwURawrn38408375018458385023841203489738570123(passcode: String!, name: String!): {digimon_type}
}}
"""

real_digimon_template = """
type {digimon_type} {{
    id: Int!,
    name: String!,
    level: String!,
    type: String!,
    attribute: String!,
    description: String!,
    flag: String!,
    tokenf0e4c2f76c58916ec258f246851bea091d14d4247a2fc3e18694461b1816e13b: String!,
    tokend743cb4b22397cf64e0117fd83d29ca1e059c698b8155a3771417e24458e2bb5: String!,
    tokenb20e3fc8e392aeae90db75a40648ad4aa87d13830ef9eb80343b960130ec2d3e: String!
}}
"""

fake_digimon_template = """
type {digimon_type} {{
    id: Int!,
    name: String!,
    level: String!,
    type: String!,
    attribute: String!,
    description: String!,
    flag: String!,
    token{token1}: String!,
    token{token2}: String!,
    token{token3}: String!
}}
"""

LIMIT = 100_000
INT_LIMIT = 2 ** 256 - 1

# generate 10^5 digimons and select one
real_id = random.randint(1, LIMIT)

def gen_token():
    return "{:064x}".format(random.randint(0, INT_LIMIT)) 

def gen_id(id):
    return "0x{:08x}".format(id)

with open("./graphql/schema.graphql", "w") as f:
    digimons = []
    for i in range(1, LIMIT):
        if i == real_id:
            digimons.append(real_digimon_template.format(
                digimon_type=f"Digimon{gen_id(i)}"
            ))
        else:
            digimons.append(fake_digimon_template.format(
                digimon_type=f"Digimon{gen_id(i)}", 
                token1=gen_token(),
                token2=gen_token(),
                token3=gen_token()
            ))
    random.shuffle(digimons)
    f.write(template.format(
        digimons="\n\n".join(digimons),
        digimon_type=f"Digimon{gen_id(real_id)}"
    ))

print(gen_id(real_id))