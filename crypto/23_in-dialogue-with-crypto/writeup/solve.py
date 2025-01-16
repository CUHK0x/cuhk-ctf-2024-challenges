from base64 import b64decode
from string import ascii_letters, digits, punctuation
from gmpy2 import gmpy2

printable = ascii_letters + digits + punctuation

def read_ciphertext():
    with open("message.txt.enc", "r") as f:
        n = f.readline()
        c = f.read()
        return c
    
ciphertext = b64decode(read_ciphertext()).decode("utf-8")

blocks = list(map(int, ciphertext[1:-1].split(', ')))

message = ""

for block in blocks:
    ok = False
    for char in printable:
        c, e = block, ord(char) // 2
        r, root_ok = gmpy2.iroot(c, e)
        if root_ok and r < (1 << 64):
            # That is the exponent
            message_part = r.to_bytes(8, "big").decode("ascii")
            message += message_part
            ok = True
            break
    if not ok:
        print("Failed")
        exit(0)

with open("message.txt", "w") as f:
    f.write(message)