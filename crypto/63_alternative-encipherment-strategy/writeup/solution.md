## \[crypto] Alternative Encipherment Strategy
> Expected Difficulty: Sophomore (Level 2)
> Final Points: ???
> Solves: ??/?? (CUHK), ??/?? (Secondary), ??/?? (Invited Teams)
> 
> When AES meets another AES.

We first have a look at what the program does:
1. Generate a random key and 2 (different) ivs
2. Tells you the ivs
3. Asks you for a message (chosen plaintext) and encrypt it with key and iv1 in CBC mode.
4. Tells you the ciphertext
5. Asks you for a ciphertext and decrypt it with key and iv2 in OFB mode.
6. Tells you the flag if the decrypted message is `b"Please give me the flag! UwU!"`

As usual for AES challenges, we go and look for the mode of operations.
![cbc encryption mode](cbc.png)
![ofb encryption mode](ofb.png)

We can observe that the top part of the 2 modes are quite similar. If you cannot see that, you can also look at wiki

> It is possible to obtain an OFB mode keystream by using CBC mode with a constant string of zeroes as input. This can be useful, because it allows the usage of fast hardware implementations of CBC mode for OFB mode encryption. 

So what we need to do is to mimic an OFB encryption with CBC mode. As suggested in the wiki excerpt above, we can use a constant string of zeroes as input. However, this will not work because the IVs are different. We need to fix the input string a little bit by setting the first block input to `iv1 XOR iv2`.

Now we get the OFB keystream, we can easily encrypt our message to get the flag.

Solve script:
```py
from pwn import *
from Crypto.Util.Padding import pad

context.log_level = "DEBUG"
with remote("localhost", 3000) as io:  # Change to remote in the real challenge
    io.recvuntil(b"iv1: ")
    iv1 = bytes.fromhex(io.recvline().strip().decode())
    io.recvuntil(b"iv2: ")
    iv2 = bytes.fromhex(io.recvline().strip().decode())

    io.sendlineafter(
        b"Enter the message to encrypt (in hex): ",
        xor(iv1, iv2).hex().encode() + b"00" * 64,
    )
    io.recvuntil(b"ciphertext1: ")
    ciphertext1 = bytes.fromhex(io.recvline().strip().decode())

    ciphertext2 = xor(pad(b"Please give me the flag! UwU!", 16), ciphertext1, cut="min")
    io.sendlineafter(b"Enter a ciphertext (in hex):", ciphertext2.hex())

    print(io.recvall())
```

Flag: **`cuhk24ctf{m4yb3_key_r3u5e_1s_r3a11y_no7_4_g0od_id3a}`**