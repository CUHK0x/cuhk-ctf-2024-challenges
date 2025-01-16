#include <stdio.h>
#include <math.h>

int main() {
    long long arr[100] = {0};
    int ptr = 0;
    for (long long i = 1; i <= 100 * 1000 * 1000; i++) {
        long long n = i * i - 1;
        long long n2 = (long long)sqrt(n);
        if (n2 * n2 > n) {
            arr[ptr] = n;
            ptr++;
            if (ptr == 100) {
                putchar('[');
                for (int j = 0; j < 100; j++) {
                    printf("%lld", arr[j]);
                    if (j != 99) {
                        printf(", ");
                    } else {
                        putchar(']');
                        putchar('\n');
                    }
                }
                return 0;
            }
        }
    }
    return 0;
}