import os
from Crypto.Util.number import isPrime as is_prime
from math import gcd


def main():
    try:
        with open('flag.txt', 'rb') as f: m = f.read()
    except:
        # Do not submit. This is not the real flag.
        m = b'flag{this_is_a_test_flag}'
    m = int.from_bytes(m, 'big')

    while True:
        p = int.from_bytes(os.urandom(1024//8), 'big')
        if p.bit_length() == 1024 and is_prime(p): break
    while True:
        q = int.from_bytes(os.urandom(1024//8), 'big')
        if p != q and q.bit_length() == 1024 and is_prime(q): break
    
    n = p * q
    phi_n = (p-1) * (q-1)

    while True:
        d = int.from_bytes(os.urandom(24)*4, 'big') # should be >64
        if gcd(d, phi_n) == 1: break

    assert d**4 > n, "vulnerable to Wiener's attack!"

    e = pow(d, -1, phi_n)
    c = pow(m, e, n)

    print(f'{n = }')
    print(f'{e = }')
    print(f'{c = }')

if __name__ == '__main__':
    main()