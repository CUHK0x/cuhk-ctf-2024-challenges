with open("flag.txt.enc", "rb") as f:
    cipher = f.read()

print("Length:", len(cipher))

prefix = b"cuhk24ctf{"
key = b""

for i in range(0, 120, 40):
    for j in range(10):
        key += (cipher[i + j] ^ prefix[j]).to_bytes(1, 'big')

# we now get the key
flag = ""
for i in range(len(cipher) // 3):
    flag += chr(cipher[i] ^ key[i % len(key)])

print(flag)
