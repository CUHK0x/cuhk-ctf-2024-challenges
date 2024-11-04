import secrets
key = secrets.token_bytes(30)
flag = open("flag.txt", "rb").read()
flag = flag + flag + flag

cipher = b""
for i in range(len(flag)):
    cipher += (flag[i] ^ key[i % len(key)]).to_bytes()

with open("flag.txt.enc", "wb") as f:
    f.write(cipher)
