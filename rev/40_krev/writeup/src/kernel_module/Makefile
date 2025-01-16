CC=gcc
ARCH=x86_64
KERNEL_ROOT=../linux
obj-m += krev.o

all:
	make CC=$(CC) ARCH=$(ARCH) -C $(KERNEL_ROOT) M=$(PWD) modules

clean:
	make CC=$(CC) ARCH=$(ARCH) -C $(KERNEL_ROOT) M=$(PWD) clean

