## In Dialogue with Crypto
> Author: chemistrying \
> Category: crypto \
> Expected Difficulty: 2 \
> Final Points: 285 \
> Solves: 6/38 (Secondary), 5/44 (CUHK), 7/8 (Invited Teams)
> 
> Trust me, it's a 1000-level crypto problem (I mean it's very beginner friendly, I guess).

This is (meant to be) a beginner-friendly crypto (since me as a non-crypto fella can also do this).

By carefully analysing the "encryption" function, we can see the logic of the code is:
1. Split the message to 8 characters a block (with padding if there isn't enough characters)
2. Set variable `e` as `key[i % len(key)]` (i.e.: just selecting the character one by one and return to the start if it runs out of characters)
3. Transform the block text to concatenation of hexadecimal of each character. For example, if the block text is `abcdefgh`, then the result would be `6162636465666768`
4. Treat the above result as numbers, raise it to the `e`-th power and modulo by `n` (a big prime number)
5. Encode the list of blocks using base 64

You can see that in step 2, `e` actually is very small and only has a few options (since the key is generated using a part of printable ASCII characters). Therefore, it is important to observe two things:
1. You can brute force the exponent and recover the whole message
2. You don't have to know the modulo, because it is useless. It can be proved that the maximum value of the block text is less than $16 ^ {16} = 2 ^ {64}$, and that of exponent is $\frac{126}{2} = 63$, so the final maximum value is less than $\left(2 ^ {64}\right) ^ {63} < 2 ^ {4096}$

Therefore, the decrypt algorithm should be:
1. Decode the list of blocks with base 64
2. Solve the equation: find $x$ such that $x^e = c$, where $e$ is the exponent you are brute forcing and $c$ is the "encrypted" text (solvable with `gmpy2.iroot` or binary search)
3. If you can solve the above equation, transform it back to hexadecimal form and extract the characters
4. Push it to the final message string
5. Repeat the above process until you have solved all ciphered block text

Solve script:
```py
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
```

The decryption only takes a few seconds.

Flag: **`cuhk24ctf{HALLO_uwu_kvnow_da_tor1cku_ando_da_essenzi_ofu_smol_exp_atta3kuwu_vary_fevvy_guud}`**