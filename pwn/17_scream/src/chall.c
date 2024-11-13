#include <stdio.h>
#include <stdlib.h>

#define BUF_SIZE 256

void fun() {
	char *buf = malloc(sizeof(char)*BUF_SIZE);
	printf("Scream all you want, at the top of your lungs!\n> ");
	fgets(buf, BUF_SIZE, stdin);
	printf(buf);
	printf("Louder!\n> ");
	fgets(buf, BUF_SIZE, stdin);
	printf(buf);
	printf("Shout like you don't care!\n> ");
	fgets(buf, BUF_SIZE, stdin);
	printf(buf);
	puts("Thanks for stopping by! Remember, your scream is always processed, so don't jump.\n");
	free(buf);
}

int main(int argc, char **argv) {
	setbuf(stdin, NULL);
	setbuf(stdout, NULL);
	fun();
	return 0;
}
