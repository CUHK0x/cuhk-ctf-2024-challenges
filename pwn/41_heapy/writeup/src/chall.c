#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

#define NOTE_NUM 0x20

typedef struct note {
	void *content;
	size_t size;
} note_t;

note_t notes[NOTE_NUM];

void init(void)
{
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stderr, NULL, _IONBF, 0);
}

void print_menu()
{
	puts("Welcome to Heapy Notes!");
	puts("Here, you are able to play with some notes :P");
	puts("1. create note");
	puts("2. delete note");
	puts("3. read note");
	puts("4. exit");
}

void readline(char *buf, size_t size)
{
	char c = 0;
	for(int i=0; i<size-1; i++) {
		int ret = read(0, &c, 1);
		if(ret < 0) exit(-1);
		if (c == '\n') {
			buf[i] = 0;
			return;
		} else {
			buf[i] = c;
		}
	}
	buf[size-1] = 0;
	return;
}

int read_int()
{
	char buf[0x10] = {0};
	readline(buf, sizeof(buf));
	return atoi(buf);
}

int get_idx()
{
	for(int i=0; i<NOTE_NUM; i++) {
		if (notes[i].content == NULL) return i;
	}
	return -1;
}

void create_note()
{
	int idx = get_idx();
	if (idx < 0) {
		puts("the notebook is full :P");
		return;
	}
	printf("size: ");
	int size = read_int();
	if (size <= 0) {
		puts("invalid size");
		exit(-1);
	}

	void *content = malloc(size);
	notes[idx].content = content;
	notes[idx].size = size;

	printf("content: ");
	readline(content, size);
}

void delete_note()
{
	printf("index: ");
	int idx = read_int();
	if (idx < 0 || idx >= NOTE_NUM) {
		puts("bad index!");
		exit(-1);
	}
	if (!notes[idx].content) {
		puts("note is not in-use!");
		exit(-1);
	}
	notes[idx].size = 0;
	free(notes[idx].content); // double free
	printf("successfully deleted note with index: %d\n", idx);
}

void read_note()
{
	printf("index: ");
	int idx = read_int();
	if (idx < 0 || idx >= NOTE_NUM) {
		puts("bad index!");
		exit(-1);
	}
	if (!notes[idx].content) {
		puts("note is not in-use!");
		exit(-1);
	}

	printf("content: ");
	write(1, notes[idx].content, notes[idx].size); // use of uninitialized data, should we patch this?
	puts("");
}

int main(int argc, char **argv, char **envp)
{
	init();

	while(1) {
		int option;
		print_menu();
		printf(">> ");
		option = read_int();
		switch(option) {
		case 1:
			create_note();
			break;
		case 2:
			delete_note();
			break;
		case 3:
			read_note();
			break;
		case 4:
			return 0;
		default:
			printf("unknown option: %d\n", option);
			exit(-1);
		}
	}
}
