#include <iostream>
#include <vector>
#include <numeric>

using namespace std;

vector<int> content = {
    13, 44, 33, 68,
    60, 66, 91, 120,
    45, 200, 99, 228,
    117, 112, 225, 64,
    204, 144, 190, 240,
    336, 176, 414, 96,
    200, 494, 405, 364,
    551, 390, 806, 8292,
    3, 381, 185, 272,
    120, 203, 219, 317
};

int main() {
    // read the list of possible characters using "choice.txt" (./solve < choice.txt)
    vector<string> possible_char(31);
    for (int i = 0; i < 31; i++) {
        cin >> possible_char[i];
    }

    // initial string (precalculated "cuhk24ctf{")
    string curr = "EWJMrtEVH]";

    // --- Start of Helper Functions ---

    // calculate the sum and product of bits for a row
    // parameter "shift" indicates the number of times the ASCII value of the character has to be shifted
    auto bit_sum_prod = [&] (int shift) {
        int ret = 0;
        for (int i = 0; i < 31; i++) {
            ret += ((curr[i] >> shift) & 1) * (i + 1);
        }
        return ret;
    };

    // checks if the sum and product of a single role is equal to Excel value
    // parameter "shift" indicates the number of times the ASCII value of the character has to be shifted
    auto check_bits = [&] (int shift) {
        return bit_sum_prod(shift) == content[33 + (6 - shift)];
    };

    // checks if the sum and product of each row is equal to Excel value
    auto check_all_bits = [&] () {
        for (int i = 0; i < 7; i++) {
            if (!check_bits(i)) return false;
        }
        return true;
    };

    // checks if the global sum value (the bottom-right one in Excel) is equal to Excel value
    auto check_global = [&] () {
        int ret = 0;
        for (int i = 0; i < 7; i++) {
            ret += bit_sum_prod(i);
        }
        ret += accumulate(content.begin(), content.begin() + 31, 0);
        return ret == content[31];
    };


    // --- End of Helper Functions ---

    auto brute = [&] (auto&& recur, int idx) -> void {
        if (idx == 31) {
            // string generated
            // do checking
            if (check_all_bits() && check_global()) {
                cout << curr << '\n';
            }
        } else {
            // try each character in that position
            for (char c : possible_char[idx]) {
                // try this character
                curr.push_back(c);

                // iterate to next position
                recur(recur, idx + 1);
                
                // revert our choice
                curr.pop_back();
            }
        }
    };

    // start brute forcing
    brute(brute, 10);
}
