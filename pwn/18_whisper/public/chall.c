#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>

#define BUF_SIZE 512

const char *voices[] = {
	"kilroy is here",
	"i love mr tong",
	"i love you",
	"what doesn't kill me makes me stronger",
	"you seem lively. did something good happen to you?",
	"i don't know everything, i only know what i know",
	"and thus, man will be forced to be free",
	"it works on my machine",
	"you love me? i am delighted, i'm sorry but you're a good person",
	"the things i love gets top priority",
	"i have no special talent. i am only passionately curious.",
};

int randint(int low, int high) {
	return rand() % high + low;
}

int main(int argc, char const *argv[])
{
	setvbuf(stdin, NULL, _IONBF, 0);
	setvbuf(stdout, NULL, _IONBF, 0);
	srand(0);
	char *s[16];
	const int n_voices = sizeof(voices) / sizeof(char*);
	for (int i = 0; i < 15; i++) {
		s[i] = malloc(512);
		strcpy(s[i], voices[randint(0, n_voices)]);
	}
	s[15] = malloc(512);
	FILE *f = fopen("/flag", "r");
	if (f == NULL) {
		puts("Something went wrong, please contact admins.");
		exit(EXIT_FAILURE);
	}
	fgets(s[15], 512, f);
	fclose(f);
	puts("It is very quiet here. Please, lowly whisper your message.");
	puts("<if you say the right word, you might get surprises.>");
	int playing = 1;
	while (playing) {
		puts("1. Get a whisper");
		puts("2. Write a whisper");
		printf("Enter your choice: ");
		int choice;
		scanf("%d", &choice);
		int idx;
		switch (choice)
		{
		case 1:
			printf("Pick a whisper: ");
			scanf("%d", &idx);
			if (idx >= 0 && idx < 15) {
				printf(s[idx]);
				putchar('\n');
			} else {
				puts("*enter a valid number please*");
			}
			break;
		case 2:
			puts("Whisper something:");
			idx = randint(0, 15);
			fgets(s[idx], BUF_SIZE, stdin);
			fgets(s[idx], BUF_SIZE, stdin);
			break;
		default:
			puts("Have a nice day!");
			playing = 0;
			break;
		}
	}
	for (int i = 0; i < 16; i++) {
		free(s[i]);
	}
	return 0;
}

