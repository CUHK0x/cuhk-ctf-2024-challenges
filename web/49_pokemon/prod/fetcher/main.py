import requests
from bs4 import BeautifulSoup
from sqlalchemy.orm import Session
import re
import argparse

import models
from database import engine

parser = argparse.ArgumentParser(description='Initialise database.')
parser.add_argument('-f', '--flag')

args = parser.parse_args()

FLAG = args.flag or "cuhk24ctf{test-flag}"

try:
    models.Pokemon.__table__.drop(engine)
except:
    pass

try:
    models.Digimon.__table__.drop(engine)
except:
    pass

models.Base.metadata.create_all(bind=engine)

html = requests.get("https://www.serebii.net/pokemon/nationalpokedex.shtml").text

soup = BeautifulSoup(html, "html.parser")

pokedex = soup.find("table", class_="dextable")

raw_pokemons = pokedex.find_all("tr")

parsed_pokemons = []

# print(raw_pokemons[4])

for raw_pokemon in raw_pokemons[2::2]:
    info = raw_pokemon.find_all("td")
    # print(re.search(r"[0-9]{4}", str(info[0].contents[0])))
    parsed_pokemons.append(models.Pokemon(
        id=int(re.search(r"[0-9]{4}", str(info[0].contents[0])).group()),
        name=info[3].find("a").contents[0],
        type1=re.search(r"([a-z]*).gif", str(info[4].find_all("a")[0].contents[0])).group(1).title(),
        type2=None if len(info[4].find_all("a")) == 1 else re.search(r"([a-z]*).gif", str(info[4].find_all("a")[1].contents[0])).group(1).title(),
        abilities=" / ".join([x.contents[0] for x in info[5].find_all("a")]),
        hp = int(info[6].contents[0]),
        attack = int(info[7].contents[0]),
        defense = int(info[8].contents[0]),
        spattack = int(info[9].contents[0]),
        spdefense = int(info[10].contents[0]),
        speed = int(info[11].contents[0])
    ))

# print(parsed_pokemons)

with Session(engine) as session:
    session.add_all(parsed_pokemons)
    session.commit()

# test pokemon code
from sqlalchemy import select
stmt = select(models.Pokemon).where(models.Pokemon.name == "Giratina")
print(session.scalars(stmt).one())
print("Pokemon database initialisation complete.")

digimons = [
    models.Digimon(
        id=1,
        name="Gammamon",
        level="Rookie",
        type="Ceratopsian",
        attribute="Virus",
        description="""An extremely rare, young white Ceratopsian Digimon that was recently discovered. Gammamon's Digivolution is said to be related to a digital signal that came from somewhere outside our galaxy. The two sturdy horns growing from its head are weapons for both attack and defense. Gammamon uses the small wings on its back to float, allowing it to fly a little. It rarely shows emotion, but it seems to grow friendly over time once it establishes an emotional bond.
Gammamon uses its special move Horn Attack to charge with its twin horns. It also uses Breaclaw to charge power into the claws of its left hand before unleashing a powerful blow.""",
        flag="Flag not here hahahahahaha",
        tokenf0e4c2f76c58916ec258f246851bea091d14d4247a2fc3e18694461b1816e13b="Flag Not Here",
        tokend743cb4b22397cf64e0117fd83d29ca1e059c698b8155a3771417e24458e2bb5="Flag Not Here",
        tokenb20e3fc8e392aeae90db75a40648ad4aa87d13830ef9eb80343b960130ec2d3e="Flag Not Here"
    ),
    models.Digimon(
        id=2,
        name="GulusGammamon",
        level="Champion",
        type="Dragon Man",
        attribute="Virus",
        description="""The evil heart hidden within Gammamon was unleashed, Digivolving it into a violent Digimon. GulusGammamon rejects outside interference and thinks of nothing but battle. When it gets its hands on the opponent in front of it, it will continue its assault until their life is extinguished. Its battles are brutal, and even if its limbs are crushed, it still continues attacking without concern.
GulusGammamon uses its special move Dark Pales to crush the enemy with dark flames gathered in its hand, or Desdemona to hurl those dark flames while preserving their might. It also uses Dead End Skewer to pierce the enemy’s vitals with its tail, annihilating them with pinpoint accuracy.""",
        flag="Flag not here hahahahahaha",
        tokenf0e4c2f76c58916ec258f246851bea091d14d4247a2fc3e18694461b1816e13b="Flag Not Here",
        tokend743cb4b22397cf64e0117fd83d29ca1e059c698b8155a3771417e24458e2bb5="Flag Not Here",
        tokenb20e3fc8e392aeae90db75a40648ad4aa87d13830ef9eb80343b960130ec2d3e="Flag Not Here"
    ),
    models.Digimon(
        id=3,
        name="Flagmon",
        level="Ultimate",
        type="Flag",
        attribute="Virus",
        description=f"Flagmon stores the flag of Pokemons in its heart with the flag of cybersecurity.",
        flag="Flag not here hahahahahaha",
        tokenf0e4c2f76c58916ec258f246851bea091d14d4247a2fc3e18694461b1816e13b="Flag Not Here",
        tokend743cb4b22397cf64e0117fd83d29ca1e059c698b8155a3771417e24458e2bb5="Flag Not Here",
        tokenb20e3fc8e392aeae90db75a40648ad4aa87d13830ef9eb80343b960130ec2d3e=FLAG
    )
]

with Session(engine) as session:
    session.add_all(digimons)
    session.commit()

# test flag code
from sqlalchemy import select
stmt = select(models.Digimon).where(models.Digimon.name == "Flagmon")
print(session.scalars(stmt).one())

print("Initialising process completed... Hopefully...")