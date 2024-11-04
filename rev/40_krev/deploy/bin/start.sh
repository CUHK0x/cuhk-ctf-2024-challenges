#!/bin/sh

qemu-system-x86_64 \
    -m 400M -smp 1 \
    -cpu qemu64,+smap,+smep \
    -kernel /home/ctf/bzImage \
    -nographic \
    -append "console=ttyS0 root=/dev/sda panic=1000 oops=panic panic_on_warn=1 kaslr smap smep tsc=unstable net.ifnames=0" \
    -initrd /home/ctf/rootfs.cpio \
    -monitor /dev/null
