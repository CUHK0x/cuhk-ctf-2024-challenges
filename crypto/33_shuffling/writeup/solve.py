from rich.progress import track
from pwn import *

r = remote('localhost', 24033)

n = int(r.recvline().decode())
c0 = int(r.recvline().decode())

c = c0
for i in range(2048):
    r.sendline(str(c).encode())
    c = pow(2, 65537, n) * c % n

lb, rb = 0, 1

hms = []
for i in track(range(2048)):
    m = int(r.recvline().decode())
    hm = bin(m).count('1') # the Hamming weight of m
    hms.append(hm)

for i in range(2047):
    lb, rb = 2*lb, 2*rb

    if hms[i] == hms[i+1]:
        # Let u = 2^i * m (mod n), then 2u < n.
        # However, there might be cases that both u and 2u has the same hamming weight even if 2u >= n. It is just unlucky.
        rb -= 1
    else:
        # this part is good
        lb += 1

lb = lb * n // 2**2047
rb = rb * n // 2**2047

for i in range(lb, rb+1): print(int.to_bytes(i, 2048//8, 'big').lstrip(b'\0'))
