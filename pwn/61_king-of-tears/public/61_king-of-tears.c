#include <stdio.h>
#include <stdlib.h>

void cry(void){
    printf("I am crying ToT\n");
    FILE *fin;
    char flag[35];
	fin = fopen("61_flag.txt", "r");
    if (fin == NULL){
        printf("If you encounter this message in the competition server, contact challenge author p3n9uin immediately by opening a ticket on the competition Discord server.\n");
        exit(999);
    }
    fgets(flag, 35, fin);
    printf("%s\n", flag);
    exit(0);
}


int main(void){
    char name[5];
    int flag = 0;
    printf("Please enter your name:");
    gets(name);
    printf("Hello %s. I do not cry.\n", name);
    return 0;
}