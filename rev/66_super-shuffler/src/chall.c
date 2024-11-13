#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

#define HAND_SIZE 8

void swap(char *a, char *b) {
    char t = *a;
    *a = *b;
    *b = t;
}

void shuffle(char *buf, int size) {
    srand(time(NULL));
    for (int i = 0; i < size; i++) {
        int idx = rand() % (size-i) + i;
        swap(buf+i, buf+idx);
    }
}

void show_hand(char *hand, int size) {
    puts("Cards at hand:");
    for (int i = 0; i < size; i++)
    {
        if (hand[i] == '0') {
            printf("  10\t");
        }
        else {
            printf("%4c\t", hand[i]);
        }
    }
    putchar('\n');
}

void win() {
    FILE* f = fopen("./flag", "r");
    if (f == NULL) {
        puts("Snap! This should not have happened. Contact FearlessSniper on Discord, with error code: 0xF0AGMI33IN3");
    }
    char flag[256];
    fgets(flag, 256, f);
    puts(flag);
}

void play() {
    char deck[] = {'0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'J', 'Q', 'K'};
    shuffle(deck, sizeof(deck));
    puts("When I play, I am always dealt a bad hand. Can you bring me good luck?");
    show_hand(deck, HAND_SIZE);
    puts("\nPick a card to get: ");
    char input[8];
    fgets(input, 8, stdin);
    while (strcmp(input, "bet\n") != 0) {
        int swap_idx;
        int args = sscanf(input, " %d", &swap_idx);
        if (args > 0) {
            swap(deck, deck+swap_idx);
        } else {
            puts("You can't do that! Play the game normally!");
        }
        show_hand(deck, HAND_SIZE);
        puts("\nPick a card to get: ");
        fgets(input, 8, stdin);
    }
    puts("Let's check if you are lucky enough...\n");
    if (*((long*)deck) == 0x70316853646e3246) {
        puts("Great fortune!\n");
        win();
    } else {
        puts("Bad luck! Guess I'm on my own...");
    }
}

int main(int argc, char const *argv[]) {
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stdout, NULL, _IONBF, 0);
    const char extra_cards[] = {'/', 'p', 's', '/', 'd', 'b', 'h', 'F', 'e', 'i', 'n', 'S'};
    // const long magic1 = 0x466862642f73702f;
    // const long magic2 = 0x536e6965;
    play();
    return 0;
}
