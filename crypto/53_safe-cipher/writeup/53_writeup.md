## Safe Cipher
> Author: chemistrying \
> Category: crypto \
> Expected Difficulty: 1 \
> Final Points: 108 \
> Solves: 15/38 (Secondary), 18/44 (CUHK), 8/8 (Invited Teams)
> 
> If you think having UGFC1000 (In Dialogue with Crypto) is too difficult, consider having more dialogue with crypto. If you brute force the cipher key, you need to try $(2^8)^{30}$ times, so it's safe.

Observe how the encryption is done:
1. Generate a 30-byte token
2. The flag is repeated 3 times
3. Perform a XOR-cipher

From `flag.txt.enc`, the length of the encryption is $120$, so the flag length is $40$. So we now know that if the token generated is `1234567890abcdefghijABCDEFGHIJ`, then:
```
XOR ciphering:
  cuhk24ctf{.............................}cuhk24ctf{.............................}cuhk24ctf{.............................}
^ 1234567890abcdefghijABCDEFGHIJ1234567890abcdefghijABCDEFGHIJ1234567890abcdefghijABCDEFGHIJ1234567890abcdefghijABCDEFGHIJ
--------------------------------------------------------------------------------------------------------------------------
  ????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????
```

Observe the fact `cuhk24ctf{` performed XOR operation with `1234567890` (first 10 characters), `abcdefghij` (41-st character to 50-th character), and `ABCDEFGHIJ` (81-st character to 90-th character). Therefore, we can retreive the key by performing XOR operation with the prefix and the characters position mentioned above.

Solve script:
```py
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
```

Flag: **`cuhk24ctf{lon9_prefis_kind_o7_iNtRe5t1n}`**
