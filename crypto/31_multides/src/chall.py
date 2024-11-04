import os
from Crypto.Cipher import DES
from Crypto.Util.Padding import pad


class MultipleDES:
    def __init__(self, key: bytes):
        self.key = key.hex().encode()

    def encrypt(self, message: bytes) -> bytes:
        ciphertext = message
        for i in range(0, len(self.key), 8):
            cipher = DES.new(self.key[i:i+8], DES.MODE_ECB)
            ciphertext = cipher.encrypt(ciphertext).hex().encode()
        return ciphertext

def main():
    try:
        with open('flag.txt', 'rb') as f: m = f.read()
    except:
        # Do not submit. This is not the real flag.
        m = b'flag{this_is_a_test_flag}'
    m = pad(m, 8)

    key = os.urandom(32)
    cipher = MultipleDES(key)
    c = cipher.encrypt(m)
    with open('flag.txt.enc', 'wb') as f:
        f.write(c)


if __name__ == '__main__':
    main()
