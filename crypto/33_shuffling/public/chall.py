from Crypto.Util.number import getPrime as get_prime
import secrets
import random


class RSA:
    def __init__(self):
        self.p, self.q = [get_prime(1024) for _ in 'pq']
        self.n = self.p * self.q
        self.phi = (self.p - 1) * (self.q - 1)
        self.e = 0x10001
        self.d = pow(self.e, -1, self.phi)

    def encrypt(self, m: int) -> int:
        return pow(m, self.e, self.n)

    def decrypt(self, c: int) -> int:
        return pow(c, self.d, self.n)


def main():
    rsa = RSA()

    try:
        with open('flag.txt', 'rb') as f: m0 = f.read()
    except:
        # Do not submit. This is not the real flag.
        m0 = b'flag{this_is_a_test_flag}'

    m0 = int.from_bytes(m0, 'big')
    c0 = rsa.encrypt(m0)

    print(rsa.n)
    print(c0)

    while True:
        c = int(input())
        m = rsa.decrypt(c)
        # I have to shuffle the bits to make your life harder
        m = format(m, 'b')
        m = list(m)
        random.shuffle(m)
        m = int(''.join(m), 2)
        print(m)


if __name__ == '__main__':
    main()
