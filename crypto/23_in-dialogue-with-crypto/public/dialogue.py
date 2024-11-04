from Crypto.Util import number
from Crypto.Random import random
from string import ascii_letters, digits, punctuation
from base64 import b64encode

p = number.getPrime(2048)
q = number.getPrime(2048)
n = p * q
printable = ascii_letters + digits + punctuation
key = ''.join([random.choice(printable) for x in range(64)])

def encrypt(m):
    m = m.ljust((len(m) + 7) // 8 * 8, b'\0')
    blks = [m[i:i+8] for i in range(0, len(m), 8)]
    c = []
    for i in range(len(blks)):
        cblk, e = int.from_bytes(blks[i], 'big'), ord(key[i % len(key)]) // 2
        c.append(pow(cblk, e, n))
    return b64encode(bytes(str(c), "ascii"))

def read_message():
    with open("message.txt", "rb") as f:
        message = f.read()
        return message

ciphertext = encrypt(read_message())
with open("message.txt.enc", "wb") as f:
    f.write(bytes(str(n) + '\n', "ascii"))
    f.write(ciphertext)