import requests, time

url = "https://github.com/CUHK-placeholder/cuhk-placeholder/commit/539{hash}"

last_fetch = 0
# loop from 5390 to 539f
for i in range(16):
    hash = "{:01x}".format(i)
    
    print(f"Checking commit prefix 539{hash}")
    # rate limit ourselves
    while time.time() - last_fetch < 1:
        pass
    last_fetch = time.time()

    # send a request
    r = requests.get(url.format(hash=hash))

    # if the request give a status code of 200, that means it's OK
    if r.status_code == 200:
        print(f"539{hash} is a valid commit")
        with open(f"539{hash}.html", "w") as f:
            f.write(r.text)
    elif r.status_code != 404:
        print("ERROR!")
        print(r.text)
        exit(0)