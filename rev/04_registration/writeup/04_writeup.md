> Expected Difficulty: Freshmen (Level 1)
> 
> One into two, two into four, and so on...

This is another introductory challenge aimed at introducing the basics of reverse engineering in CTF. This time involving the use of registers for disassembling the binary.
The binary's expects us to input 4 characters. It then returns to us with a line called "bye!".
Apparently this is not we want.

If we decompile the program, then we can see that the main gets a 64-bit random double from the `getrandom()` function, which the seed resets every 60 seconds.
After that it split te lower 32-bit value into four 8-bit characters, then XOR each of it with `c`, `u`, `h`, `k` respectively.
First we know that if $A\oplus B= C$, then $C\oplus B = A$.

How to get this random value from this `getrandom()`?
Turns out that normally for every function, the function's return value is being stored in the `eax` register. So by the time the function returns, we can just grab value inside the register and use it for our own purposes!

If we call gdb and disassemble the main function, we can see at `main+30`, the `eax` register has been called. So with the following commands, we can get the return value from the `getrandom()` function.
```
gdb 04_chall.exe
pwndbg> break *main+30
pwndbg> r
pwndbg> p $eax

```

The value from gdb is a 64-bit signed integer. We then need a simple solve script for automating the progress for us:

```
#!/usr/bin/python3

from pwn import *
from datetime import datetime

dt = datetime.today()
seconds = dt.timestamp()/60
conn = remote("localhost", 24104)
input_number = int(input("Number:"))

payloadA = chr((input_number & 0x7F) ^ 99)
payloadB = chr(((input_number >> 8) & 0x7F) ^ 117)
payloadC = chr(((input_number >> 16) & 0x7F) ^ 104)
payloadD = chr(((input_number >> 24) & 0x7F) ^ 107)

conn.recvuntil(b"Enter four characters: ")
payload = (f"{payloadA} {payloadB} {payloadC} {payloadD}").encode("ascii")
conn.sendline(payload)
conn.interactive()
```

if we execute the gdb commands and the above solve script in the same minute, we then can get the flag.

Flag: `cuhk24ctf{eax_n_xor_OH_THEY_LEAK_SECRETSSSSSS_qbGxXo5}`