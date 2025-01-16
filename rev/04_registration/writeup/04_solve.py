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
# conn.sendlineafter(b':', buf)
#print("payload|" + f"{payloadA} {payloadB} {payloadC} {payloadD}")
conn.recvuntil(b"Enter four characters: ")
payload = (f"{payloadA} {payloadB} {payloadC} {payloadD}").encode("ascii")
conn.sendline(payload)
conn.interactive()