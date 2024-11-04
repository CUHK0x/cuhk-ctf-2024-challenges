#include <stdio.h>
#include <math.h>
#include <string.h>
#include <time.h>
#include <stdlib.h>

const char* nouns[12] = {
    "silly little old-fashioned happy witch", 
    "RNGesus christ",
    "nerd",
    "weeb",
    "fuzzy little creature",
    "checkmate",
    "normie",
    "hacker",
    "'smart' coder",
    "that random student who got 5** in Maths but failed in this simple math",
    "touch grass enthusiast",
    "seems like you can't read properly"
};

int is_unique(long long n, int* used, int limit) {
    for (int i = 0; i < limit; i++) {
        if (used[i] == n) {
            return 0;
        }
    }
    return 1;
}

int main() {
    srand(time(NULL));

    int chance = 100;
    int used[100] = {0}, ptr = 0;
    while (chance > 0) {
        printf("Give me a%s non-negative integer N, I will help you find the square root of N rounded down to the nearest integer (0 <= N <= 10^16)!\n", chance == 99 ? "" : "nother");
        fflush(stdout);

        char str[20] = {0};
        char* endptr;
        fgets(str, sizeof(str), stdin);
        size_t len = strlen(str);
        while (len--) {
            if (str[len] == '\r' || str[len] == '\n') str[len] = '\0';
            else break;
        }

        // determine if it is a number
        long long n = strtoll(str, &endptr, 10);
        if (endptr == str || *endptr != '\0') {
            printf("Hey, that is not a number, %s!\n", nouns[rand() % 12]);
            fflush(stdout);
            return 0;
        }

        // check unique
        if (!is_unique(n, used, ptr)) {
            printf("Hey, you try to trick me by reusing your previous numbers, %s!\n", nouns[rand() % 12]);
            fflush(stdout);
            return 0;
        }
        used[ptr++] = n;

        // check if it's in range
        if (!(0 <= n && n <= 10LL * 1000 * 1000 * 1000 * 1000 * 1000)) {
            printf("Hey, that's not in my range of computation, %s!\n", nouns[rand() % 12]);
            fflush(stdout);
            return 0;
        }

        // check function
        long long k = (long long)sqrt(n);
        if (k * k <= n && (k + 1) * (k + 1) > n) {
            printf("%lld * %lld <= %lld\n", k, k, n);
            printf("Yay, I did it, mother! I'm still a successful person!\n");
            fflush(stdout);
            return 0;
        } else {
            printf("%lld * %lld...\n", k, k);
            printf("WHAT... I calculated wrongly...\n");

            chance--;
            if (chance > 0) {
                printf("That's impossible, I believed that the program was just affected by cosmic ray and caused a bit flip!");
                printf("Give me one more chance (%d chances left)!", chance);
            } else {
                printf("Ok I give up, %s. I will give you the flag as a compensation...\n", nouns[rand() % 12]);
                
                FILE *f = fopen("flag.txt", "r");
                if (f == NULL) {
                    printf("Here is the flag: cuhk24ctf{test-flag}\n");
                } else {
                    char flag[100] = {0};
                    fgets(flag, sizeof(flag), f);

                    printf("Here is the flag: %s\n", flag);
                }
            }
            fflush(stdout);
        }
    }

    return 0;
}