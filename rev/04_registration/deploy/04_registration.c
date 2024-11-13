#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <time.h>
#include <string.h>

double getrandom(){
    char chunk_array[4];
    double randomer = 0;
    srand((time(NULL)/60));
    while (1){
        randomer = (double)rand() / RAND_MAX;
        // Convert the double to a uint64_t
        uint64_t double_bits = *((uint64_t*)&randomer);
        // Extract the 8-bit chunks and cast them to char
        chunk_array[0] = (char)(double_bits & 0x7F);
        chunk_array[1] = (char)((double_bits >> 8) & 0x7F);
        chunk_array[2] = (char)((double_bits >> 16) & 0x7F);
        chunk_array[3] = (char)((double_bits >> 24) & 0x7F);
        //printf("%d %d %d %d\n", chunk_array[0], chunk_array[1], chunk_array[2], chunk_array[3]);
        //printf("%c %c %c %c\n", chunk_array[0], chunk_array[1], chunk_array[2], chunk_array[3]);
        if (chunk_array[0] <= 96 && chunk_array[1] <= 96 && chunk_array[2] <= 96 && chunk_array[3] <= 96) {
            //printf("Generate random number:\n%d %d %d %d\n", chunk_array[0], chunk_array[1], chunk_array[2], chunk_array[3]);
            //printf("%c %c %c %c\n===\n", chunk_array[0], chunk_array[1], chunk_array[2], chunk_array[3]);
            break;
        }

    }
    return randomer;
}

int main(int argc, char *argv) {
    double random_number = getrandom();

    char user_char_array[4];
    printf("Enter four characters: ");
    scanf("%c %c %c %c", &user_char_array[0], &user_char_array[1], &user_char_array[2], &user_char_array[3]);
    
    uint64_t input_bits = *((uint64_t*)&random_number);
    char result_array[4];    

    result_array[0] = user_char_array[0] ^ (input_bits & 0x7F);
    result_array[1] = user_char_array[1] ^ ((input_bits >> 8) & 0x7F);
    result_array[2] = user_char_array[2] ^ ((input_bits >> 16) & 0x7F);
    result_array[3] = user_char_array[3] ^ ((input_bits >> 24) & 0x7F);

    // Check if the result matches the binary representation of the pre-determined string
    const char* target_string = "cuhk";
    if (memcmp(result_array, target_string, 4) == 0) {
        char flag[55];
        FILE *fin;
        fin = fopen("04_flag.txt", "r");
        if (fin == NULL){
            printf("If you encounter this message in the competition server, contact challenge author p3n9uin immediately by opening a ticket on the competition Discord server.\n");
            exit(999);
        }
        fgets(flag, 55, fin);
        printf("%s\n", flag);
    } else {
        printf("bye!");
    }

}