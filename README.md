# CUHK CTF 2024

## Description
Below is the challenges in CUHK CTF 2024 held on 12-13 October. Writeups are redacted until the writeup workshop.

## Folder Structure Explanation
Challenge folders are placed under their corresponding categories (`crypto`, `forens`, `misc`, `pwn`, `rev`, `web`). Under each challenge folder, `public` folder represents the materials given to the participants. `deploy` folder contains secrets used during deployment in the challenge server. `README.md` contains challenge description and necessary challenge info. There is also a `[id]_flag.txt` for the flag used in the challenge.

## Running Challenge Server
Some challenges have a challenge remote server. You can spin up one by doing the following procedures. However, please note that you shouldn't expose the challenges to the public or your machine might be compromised. It is highly recommended to do it in a virtual machine.

### Linux
Run the run challenge script. The challenge will be built automatically. Note that you must install docker compose (for both Linux and Windows). Also note that you might need root permission to run docker if you haven't setup docker group permissions.
```bash
./run_chall.sh CATEGORY/DIRECTORY_NAME
```
For example, if you want to run challenge "Indonesian Culture", you should type `./run_chall.sh rev/03_indonesian-culture`. 

To stop the server:
```bash
./stop_chall.sh CATEGORY/DIRECTORY_NAME
```

To rebuild the server to sync the source code update:
```bash
./run_chall.sh CATEGORY/DIRECTORY_NAME --build
```

To create the production folder only:
```bash
./make_chall.sh CATEGORY/DIRECTORY_NAME
```

### Windows
The process is similar but batch scripts are used instead.

To run the server:
```bat
run_chall.bat CATEGORY\DIRECTORY_NAME
```

To stop the server:
```bat
stop_chall.bat CATEGORY\DIRECTORY_NAME
```

To rebuild the server to sync the source code update:
```bat
run_chall.bat CATEGORY\DIRECTORY_NAME --build
```

To create the production folder only:
```bat
make_chall.bat CATEGORY\DIRECTORY_NAME
```

### Docker Compose Tips
To read the logs of the server, you can change directory to the production folder and type:
```bash
docker compose logs
```

## Challenges
| Index | Challenge Name            | Author    | Category | Difficulty | Solves (Secondary / CUHK / Inivited) |
| ----- | ----- | ----- | ----- | ----- | ----- |
| 01    | Does it ring a bell? | p3n9uin | `misc` | 3 | 2 / 1 / 5 |
| 02    | Penguin Habitat | p3n9uin | `misc` | 2 | 6 / 8 / 3 |
| 03    | Indonesian Culture | p3n9uin | `rev` | 1 | 9 / 15 / 7 |
| 04    | Registration | p3n9uin | `rev` | 1 | 3 / 0 / 3 |
| 13    | XClass | F21endSh1p | `web` | 2 | 7 / 5 / 2 |
| 14    | friends | F21endSh1p | `web` | 4 | 0 / 0 / 0 |
| 16    | Alice, Bob and Mallory | chemistrying | `rev` | 2 | 10 / 17 / 7 |
| 17    | Scream | F21endSh1p | `pwn` | 4 | 0 / 0 / 1 |
| 18    | Whisper | F21endSh1p | `pwn` | 2 | 6 / 8 / 6 |
| 19    | Placeholder | chemistrying | `misc` | 3 | 10 / 8 / 7 |
| 20    | Burpmon | chemistrying | `web` | 1 | 25 / 38 / 8 |
| 21    | Telepathy | chemistrying | `web` | 3 | 0 / 0 / 0 |
| 22    | Secret Server | chemistrying | `misc` | 1 | 14 / 12 / 6 |
| 23    | In Dialogue with Crypto | chemistrying | `crypto` | 2 | 6 / 5 / 7 |
| 25    | Ho Grass Cat | rain251 | `forens` | 1 | 24 / 27 / 7 |
| 26    | I go to main campus on foot | rain251 | `forens` | 2 | 0 / 3 / 2 |
| 27    | Secret Menu | rain251 | `forens` | 1 | 3 / 8 / 6 |
| 30    | Flags Warehouse | rain251 | `misc` | 1 | 32 / 40 / 7 |
| 31    | MultiDES | Mystiz | `crypto` | 3 | 1 / 1 / 1 |
| 32    | Winner Winner | Mystiz | `crypto` | 3 | 0 / 1 / 3 |
| 33    | Shuffling | Mystiz | `crypto` | 4 | 0 / 1 / 0 |
| 37    | baby-rop | ky1ebot | `pwn` | 3 | 0 / 0 / 6 |
| 38    | baby-aarch64 | ky1ebot | `pwn` | 3 | 0 / 0 / 1 |
| 40    | krev | ky1ebot | `rev` | 5 | 8 / 3 / 2 |
| 41    | heapy | ky1ebot | `pwn` | 5 | 0 / 0 / 1 |
| 42    | children-aarch64 | ky1ebot | `pwn` | 4 | 0 / 0 / 1 |
| 46    | Meandering Binaries | FieryRMS | `forens` | 3 | 1 / 1 / 0 |
| 47    | Cryptic Tears | FieryRMS | `rev` | 3 | 0 / 0 / 1 |
| 49    | Pokemon | chemistrying | `web` | 4 | 1 / 1 / 1 |
| 51    | Network Traffic Analyst | chemistrying | `web` | 1 | 21 / 26 / 7 |
| 52    | Marker | chemistrying | `forens` | 2 | 27 / 25 / 8 |
| 53    | Safe Cipher | chemistrying | `crypto` | 1 | 15 / 18 / 8 |
| 54    | Resize to Win | chemistrying | `misc` | 1 | 15 / 12 / 7 |
| 56    | Laboratory Safety | rain251 | `crypto` | 1 | 30 / 34 / 8 |
| 58    | After I accidentally deleted my super secret stash, I panicked and went ahead to shrink my whole hard drive into a file with Doraemon's minifying torch. ~Hunting treasures with my overpowered forensics skill~ | F21endSh1p | `forens` | 3 | 0 / 0 / 2 |
| 61    | King of Tears | p3n9uin, F21enSh1p | `pwn` | 1 | 7 / 14 / 7 |
| 63    | Alternative Encipherment Strategy | Jackylkk2003 | `crypto` | 2 | 2 / 4 / 5 | 
| 66    | Super Shuffler | F21endSh1p | `rev` | 2 | 3 / 0 / 3 |
| 98    | Freshman Orientation | p3n9uin | `feedback` | 0 | 38 / 44 / 8 |
| 99    | Graduation | p3n9uin | `feedback` | 0 | 33 / 42 / 8 |
