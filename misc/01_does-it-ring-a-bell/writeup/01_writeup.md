## \[misc] Does it ring a bell?
> Expected Difficulty: Level 3
> 
> **Specific flag format applies: `cuhk24ctf{[a-zA-Z0-9_]+}`**
> p3n9uin is too lazy, he just decided that modifying [one particular challenge](https://github.com/blackb6a/hkcert-ctf-2021-challenges/tree/master/36-excel) and performing ROT47 on the whole outcome would be enough to deter participants from getting the flag...

So a spreadsheet file is given as the source file. 
However, all we see is a empty sheet! No, that's neither your fault nor your your computer's fault.
Since Excel supports hidden sheets, we can check if there are hidden sheets in the Excel file by using the sheet selector.

Inside the sheet `CipheredFlag` that is now revealed, are large boxes at the top part, and red "Check" boxes at the bottom. The instruction at the first row of the spreadsheet file tells us to check the flag at the top boxes.
Whilst randomly exploring the behaviour of the spreadsheet file, we can see that filling in some letters onto the top boxes will change the colour of some "Check" boxes from red to green, whilst some of the "Check" boxes will turn from green back to red if we fill specific top boxes with specific letters.
Experienced CTF players may realize that the challenge is made by ~~plagiarising~~ using a similar logic to the [HKCERT CTF 2021 "Step by Step" challenge](https://github.com/blackb6a/hkcert-ctf-2021-challenges/tree/master/36-excel), in which the original challenge has the flag directly inside the spreadsheet if you fill in the correct flag into the blanks. *(Kudos to cire_meat_pop, for creating the original challenge!)*
The link to this challenge is also placed in the description of this challenge. Maybe knowing how to solve the "Step by Step" challenge first would be advantageous?

By obtaining the correct numbers from the "Manage Rules" section of the spreadsheet file, we can find the correct number of each "Check" box.
With the cells' formulas using BITAND with 1, and then BITSHIFT by 0-6 bits, it is clear that the binary ASCII value of the character typed in the top box are reflected in the middle boxes. 
Next, last, the sum at the bottom is multiplied that by both the row and the column number.

As for how to approach the cells, we can check that the formula for cell `L23` is `=D5+D9+D12`. And the criteria for that cell to change to green is that the value of the sum is 3. This means that each of `D5`,`D9` and `D12` has a value of 1.

Since we already know that ROT47 is used to encrypt the whole flag and that the first letter is `E`, we can precompute the first 10 characters `cuhk24ctf{` so that we get prefix `EWJMrtEVH]` (note that you don't exactly shift 47 times, you have to shift 64 times to shift the first character to `E`).

For the original challenge, [writing a script for bruteforcing each character](https://ctftime.org/writeup/31555) is possible, the solve script can be found after some quick search on the Internet/CTFTime. However, the original solve script would not get you very far, since during testing we have already found that there would be too many possible combinations, we have specifically reduced the search space for you by specifying the flag format in RegEx.

Since we know that letter `c` shifts to letter `E`, we now also know that the next character `d` shifts to letter `F`; the next-next character `e` shifts to letter `G`, and so on. Therefore, we now get the character set after ROT47 encryption:

```
Original charset space:
abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890_{}

Encrypted charset space:
CDEFGHIJKLMNOPQRSTUVWXYZ[\#$%&'()*+,-./0123456789:;<qrstuvwxypA]_
```

We can use this encrypted charset space to generate all possible characters for each column (i.e: index) by:
1. Loop through each character in the "encrypted charset space"
2. Check its value after sum and product
3. If the value is equal, push it to the list
4. Output the choices for each position

(Solve script by `chemistrying`)
```py
content = [
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
]

# Note (one-based):
# Cell 1-31 = Sum and product of bits (for each column)
# Cell 32 = Global sum
# Cell 33 = Strange sum
# Cell 34+ = Sum and product of bits (for each row)

# calculate sum and product of bits
def sum_prod(x):
    ret = 0
    for i in range(7, 0, -1):
        ret += i * (x & 1)
        x >>= 1
    return ret

possible_char = []
# loop from 1st character to 31st character (you can just start from 11th character, to be honest)
for i in range(31):
    possible_char.append([])
    for j in [ord(x) for x in "CDEFGHIJKLMNOPQRSTUVWXYZ[\#$%&'()*+,-./0123456789:;<qrstuvwxypA]_"]:
        # simulate the formula in Excel
        val = sum_prod(j) * (i + 1)
        if val == content[i]:
            # push to possible charset list
            possible_char[i].append(chr(j))

# emostrate the charset
print('\n'.join([''.join(x) for x in possible_char]))

# write to a file for later usage
with open("choice.txt", "w") as f:
    f.write('\n'.join([''.join(x) for x in possible_char]))

# calculate possibilities from the 11th character to 31th character to verify that we can brute force within reasonable time
poss = 1
for arr in possible_char[10:]:
    poss *= len(arr)
print(poss)
```

You can see that we have around $10^9$ of possbilities, which can be brute force within reasonable time (depends on your implementation and language choice). 

(Solve script by `chemistrying`)
```cpp
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
```

Finally, this will leave you with 5 possible combinations.
```
EWJMrtEVH]TG8A#PFA416AKPAG:Esq_
EWJMrtEVH]T+TA#PFA416AKPAGV)sq_
EWJMrtEVH]Ts8A#PrA416AKPAG:EGq_
EWJMrtEVH]8+TA#P*A416AKPAGVEsq_
EWJMrtEVH]8sTA#PrA416AKPAGVE+q_
```
Just perform ROT47 on all 5 of them and then try all 5 to see which one is the real flag.

Some remarks from the script author:
1. The above 2-part script can be merged into single one.
2. The second part brute force can be further constant optimized.
3. The reason why there are 2 scripts is because originally I expect to brute force in Python. However, seeing that the number of possibilities is larger than $10^9$, it would be way faster to use C++ to brute force.
4. If you solved the challenge using `z3` please definitely let us know, we want to know too.

Flag: **`cuhk24ctf{reV_And_ROT_in_eXc31}`**
