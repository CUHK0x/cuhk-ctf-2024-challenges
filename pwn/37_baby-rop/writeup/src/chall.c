#include <stdio.h>
#include <unistd.h>

void duh()
{
	printf(".");
	usleep(1000*800);
	printf(".");
	usleep(1000*800);
	printf(".");
	usleep(1000*800);
	puts("");
}

void init()
{
	setvbuf(stdin, NULL, _IONBF, 0);
	setvbuf(stdout, NULL, _IONBF, 0);
}

int main()
{
	init();

	puts("Hello fellow hackers!");
	duh();
	puts("This is kylebot!");
	duh();
	puts("I'm going to give you a gift!");
	duh();

	printf("%p\n", (void*)puts);
	puts("Now please open the gift, I'm soooooo exicted for it!");
	printf(">>");

	char c[0x10];
	read(0, c, 0x100);
}
