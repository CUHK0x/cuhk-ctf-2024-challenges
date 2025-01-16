# TL;DR
*I already spent too much time on this so only a short one*
```
Arch:       amd64-64-little
RELRO:      Full RELRO
Stack:      Canary found
NX:         NX enabled
PIE:        PIE enabled
Stripped:   No
```
## Vuln
The vulnerability is obvious: `printf` called on a user supplied string, 3 times. This means the
user can read/write arbitrary memory. The problem, however, is all protections are on, and the
string is read to the heap. That means we can't easily poison GOT table like usual challenges.

My solution is to make use of pointers on the stack, to the stack to write to locations on the
stack, ROP, and RCE.

## Solve steps
0. Leak the addresses of LIBC functions to determine GLIBC version. *Not tested but can be done
   reasonably easily*
1. Leak exe, glibc, and stack address
2. Write return address of `fun` to `fun`
3. Write `NULL` to ROP chain stack
4. Write return address of `fun` to `pop rdi; ret` gadget
5. Write end of ROP chain return address to `one_gadget`
6. Enjoy shell

## Why so hard?
1. There are only 3 one_gadgets in the running glibc
2. The first two is not (easily) usable; `rdi` is set to `0xF` when program exits, which can't
   spawn a shell --> Have to build a ROP chain manually to setup `rdi`
3. The format string is stored on the heap, meaning that we cannot supply our own pointers to
   write to the stack.
