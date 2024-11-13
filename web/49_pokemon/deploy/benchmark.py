import aiohttp
import asyncio
import time
from random import choices, randint

start_time = time.time()

pokemons = ["Giratina", "Palkia", "Dialga", "Darkrai", "Koraidon", "Mewtwo", "Dragonite", "Lucario", "Riolu", "Mew", "Sharpedo", "Rayquaza", "Kyogre", "Groudon"]

# async def post_request(session, url):
#     async with session.post(url, json={"pokemons": ["Giratina\") { id } __schema { types { name } } _2:pokemon(name:\"Dialga "], "compares": ['id', 'type1', 'type2', 'hp']}) as resp:
#         await resp.json()

async def post_request(session, url):
    async with session.post(url, json={"pokemons": choices(pokemons, k=randint(1, len(pokemons))), "compares": ['id', 'type1', 'type2', 'hp']}) as resp:
        await resp.text()
        # print(text)

async def main():
    async with aiohttp.ClientSession() as session:
        tasks = []
        for i in range(100):
            tasks.append(asyncio.ensure_future(post_request(session, 'http://192.168.0.143:24049/api/query')))
        
        await asyncio.gather(*tasks)

asyncio.run(main())
print("--- %s seconds ---" % (time.time() - start_time))