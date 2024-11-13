#!/bin/sh

cd ..
python3 fetcher/generate_schema.py graphql_for_digimon_and_pokemon
python3 fetcher/main.py -f $(cat ../49_flag.txt)