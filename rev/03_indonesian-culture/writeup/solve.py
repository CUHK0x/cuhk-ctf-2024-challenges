from pwn import *
from datetime import datetime, timezone, timedelta

conn = remote("localhost", 24003)

today = datetime.now(tz=timezone(timedelta(hours=0)))
conn.recvuntil(b"Enter the password: ")
conn.send(bytes(f"p3n9uinIsAw3s0ne{today.strftime('%d/%m/%Y')}\n", "ascii"))
print(conn.recvall().decode("ascii"))