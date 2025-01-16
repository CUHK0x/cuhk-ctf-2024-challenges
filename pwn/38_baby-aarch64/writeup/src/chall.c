#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <unistd.h>
#include <fcntl.h>
#include <assert.h>
#include <sys/mman.h>
#include <sys/sendfile.h>

__attribute__((constructor))
void init(void)
{
    // disable buffering
    setbuf(stdin, NULL);
    setbuf(stdout, NULL);
    setbuf(stderr, NULL);
}

const char leading[] = "Your input is: \n";

void func(void)
{
	int ret;
    char buf[0x400];
	char *ptr = buf;
    int lead_len = 0;

    // intros

    // clear buffer
    memset(buf, 0, sizeof(buf));

    // insert leading trash
    strcpy(buf, leading);
    lead_len = strlen(leading);
    ptr = &buf[lead_len];// reset buf pointer

    // read input
    ret = read(0, ptr, sizeof(buf)-lead_len-1);
	//if(ret <= 0 || strstr(ptr, "END")) exit(-1);
	if(ret <= 0) exit(-1);

    printf(ptr);

    // read input
    ret = read(0, ptr, sizeof(buf)-lead_len-1);
	//if(ret <= 0 || strstr(ptr, "END")) exit(-1);
	if(ret <= 0) exit(-1);

    printf(ptr);
}

int main(int argc, char **argv, char **envp)
{
    assert(argc > 0);

    // -----------------------------------------//

    printf("###\n");
    printf("### Welcome to %s!\n", argv[0]);
    printf("###\n");
    printf("\n");
    // -----------------------------------------//

    // challenge introduction
    puts("pwn.college is fun and all, but it runs on the wrong architecture. Let's help it fix the issue!");
    puts("(and yes, this challenge is inspired by one of the challenge on pwn.college that's written by me :P)");

    // -----------------------------------------//

    // for (int i = 3; i < 10000; i++) close(i);
    for (char **a = argv; *a != NULL; a++) memset(*a, 0, strlen(*a));
    for (char **a = envp; *a != NULL; a++) memset(*a, 0, strlen(*a));
    // -----------------------------------------//

    func();

    // -----------------------------------------//

}
