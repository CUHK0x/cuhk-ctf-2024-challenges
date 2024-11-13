import itertools
from Crypto.Cipher import DES
from tqdm import tqdm

HEXCHARS = set(b'0123456789abcdef')
IS_GOOD = [i in HEXCHARS for i in range(256)]

with open('flag.txt.enc', 'rb') as f:
    c = f.read()

for n in range(1, 8):
    c = bytes.fromhex(c.decode())
    c0 = c[:8] # as a teaser
    for key in tqdm(itertools.product(b'abdf02468', repeat=8), total=9**8):
        cipher = DES.new(key, DES.MODE_ECB) # seems okay for pypy3 to supply key as a list of bytes...
        t0 = cipher.decrypt(c0)
        if not all(IS_GOOD[tc] for tc in t0): continue
        t = cipher.decrypt(c)
        if not all(IS_GOOD[tc] for tc in t): continue
        print(f'{n}th key recovered: {key}, message: {t}')
        break
    c = t

t = bytes.fromhex(t.decode())
t0 = t[:8]
for key in tqdm(itertools.product(b'abdf02468', repeat=8), total=9**8):
    cipher = DES.new(key, DES.MODE_ECB)
    m0 = cipher.decrypt(t0)
    if m0 != b'cuhk24ct': continue
    m = cipher.decrypt(t)
    print(f'8th key recovered: {key}, message: {m}')


