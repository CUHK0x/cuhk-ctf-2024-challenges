#include <string.h>
#include <fstream>
#include <iostream>
#include <istream>

#ifdef DEV
#include <chrono>
#include <sstream>
#endif

using namespace std;

typedef unsigned long long ull;

#define BLOCK_SIZE 8
#define REPETITIONS 8

#ifdef DEV
void print_block(ull block[])
{
    for (int i = 0; i < BLOCK_SIZE; i++)
    {
        for (int j = 0; j < BLOCK_SIZE; j++)
            cout << (block[i] >> (BLOCK_SIZE - j - 1) & 1);
        cout << endl;
    }
    cout << endl << endl;
}
#endif

#ifdef DEV
/**
 * @brief horizontal circular shift
 *
 * @param val value to shift
 * @param amt amount to shift
 * @param reverse reverse the shift
 */
void h(ull &val, int amt, bool reverse = false)
#else
void h(ull &val, int amt)
#endif
{
    amt %= BLOCK_SIZE;

#ifdef DEV
    if (reverse) amt = BLOCK_SIZE - amt;
#endif

    val = (val >> amt | val << (BLOCK_SIZE - amt)) & ((1ULL << BLOCK_SIZE) - 1);
}

/**
 * @brief GCD of two numbers
 */
int g(int a, int b)
{
    if (b == 0) return a;
    return g(b, a % b);
}

/**
 * @brief LCM of two numbers
 */
int l(int a, int b)
{
    return a * (b / g(a, b));
}

ull min(ull a, ull b)
{
    return a < b ? a : b;
}

int min(int a, int b)
{
    return a < b ? a : b;
}

#ifdef DEV
/**
 * @brief horizontal circular shift
 *
 * @param val value to shift
 * @param amt amount to shift
 * @param pos row to shift
 * @param reverse reverse the shift
 */
void h(ull block[], int amt, int pos, bool reverse = false)
#else
void h(ull b[], int amt, int pos)
#endif
{
    pos %= BLOCK_SIZE;

#ifdef DEV
    h(block[pos], amt, reverse);
#else
    h(b[pos], amt);
#endif
}

#ifdef DEV
/**
 * @brief vertical circular shift
 *
 * @param b block of data
 * @param amt amount to shift
 * @param pos column to shift
 * @param reverse reverse the shift
 */
void v(ull block[], int amt, int pos, bool reverse = false)
#else
void v(ull block[], int amt, int pos)
#endif
{
    amt %= BLOCK_SIZE;
    pos %= BLOCK_SIZE;
    ull temp = 0;
    // get the column
    for (int i = 0; i < BLOCK_SIZE; i++) temp |= (block[i] >> pos & 1) << i;

#ifdef DEV
    // regular horizontal shift
    h(temp, amt, reverse);
#else
    h(temp, amt);
#endif
    // set the column
    for (int i = 0; i < BLOCK_SIZE; i++)
    {
        block[i] = (((block[i] & ~(1ULL << pos)) |
                     ((temp & (1ull << i)) >> i << pos)) &
                    ((1ULL << BLOCK_SIZE) - 1));
    }
}

/**
 * @brief XOR operation
 *
 * @param b block of data
 * @param amt xor value
 * @param pos row to xor
 */
void x(ull block[], int amt, int pos)
{
    pos %= BLOCK_SIZE;
    block[pos] = (block[pos] ^ amt) & ((1ULL << BLOCK_SIZE) - 1);
}

// compare two arrays
bool arrcmp(ull a[], ull b[])
{
    for (int i = 0; i < BLOCK_SIZE; i++)
        if (a[i] != b[i]) return false;
    return true;
}
/**
 * @brief get_password
 *
 * @return string password
 */
string gp()
{
    string password = "";
    while (true)
    {
        cout << "Enter password: ";
        getline(cin, password);
        if (password.back() == '\r') password.pop_back();
        if (password.length() >= 8) break;

        cout << "Password must be at least 8 characters long." << endl;
    }
    return password;
}

/**
 * @brief get input file path
 *
 * @param prompt prompt message
 * @return ifstream
 */
ifstream gi(string prompt)
{
    while (true)
    {
        string input;
        cout << prompt << ": ";
        getline(cin, input);
        if (input.back() == '\r') input.pop_back();
        ifstream file(input, ios::binary);
        if (file.is_open()) return file;
        cout << "File not found." << endl;
    }
}
/**
 * @brief get output file path
 *
 * @return ofstream
 */
ofstream go()
{
    while (true)
    {
        string output;
        cout << "Enter output file: ";
        getline(cin, output);
        if (output.back() == '\r') output.pop_back();
        ofstream file(output, ios::binary);
        if (file.is_open()) return file;
        cout << "File not found." << endl;
    }
}

/**
 * @brief Encrypt block of data
 */
void e(ull block[], string pass)
{
    int rep = l(BLOCK_SIZE * 2, pass.length()) * REPETITIONS;

    for (int i = 0; i < rep; i++)
    {
        if (i & 1) v(block, pass[i % pass.length()], i / 2);
        else h(block, pass[i % pass.length()], i / 2);

        x(block, pass[i % pass.length()], i / 2);
    }
}

/**
 * @brief block_input_output
 * reads data and returns block of data
 */
struct bio {
    size_t file_size;
    ull **blocks;
    int block_count;

    bio(istream &inpt, bool trim = true)
    {
        unsigned char *file_data;
        inpt.seekg(0, ios::end);
        file_size = inpt.tellg();
        inpt.seekg(0, ios::beg);

        file_data = new unsigned char[file_size];

        inpt.read(reinterpret_cast<char *>(file_data), file_size);

        block_count = (file_size * 8 + BLOCK_SIZE * BLOCK_SIZE - 1) /
                      (BLOCK_SIZE * BLOCK_SIZE);

        blocks = new ull *[block_count];
        ull offset = 0;

        for (int i = 0; i < block_count; i++)
        {
            blocks[i] = new ull[BLOCK_SIZE];

            for (int j = 0; j < BLOCK_SIZE; j++)
            {
                blocks[i][j] = gnnb(BLOCK_SIZE, file_data, offset);
                offset += BLOCK_SIZE;
            }
        }

        if (trim)
        {
            bool del = true;
            for (int i = 0; i < BLOCK_SIZE; i++)
                if (blocks[block_count - 1][i] != 0) del = false;

            if (del)
            {
                delete blocks[block_count - 1];
                block_count--;
            }
        }

        delete file_data;
    }
    ~bio()
    {
        for (int i = 0; i < block_count; i++) delete blocks[i];
        delete blocks;
    }

    /**
     * @brief get block count
     *
     * @return int
     */
    int gbc() { return block_count; }

    /**
     * @brief get byte at offset/idx
     *
     * @param file_data
     * @param byte_offset
     * @return int
     */
    int gby(unsigned char *file_data, ull byte_offset)
    {
        if (byte_offset >= file_size) return 0;
        return file_data[byte_offset];
    }

    /**
     * @brief get next n bits
     */
    ull gnnb(ull n, unsigned char *file_data, ull offset)
    {
        ull result = 0;
        ull byte_offset = offset / 8;
        offset %= 8;

        while (n > 0)
        {
            ull curr_write = min(8 - offset, n);
            ull mask = (1ULL << curr_write) - 1;
            ull masked = gby(file_data, byte_offset) &
                         (mask << (8 - offset - curr_write));

            result |= masked >> (8 - offset - curr_write) << (n - curr_write);

            n -= curr_write;
            offset += curr_write;
            byte_offset += offset / 8;
            offset %= 8;
        }
        return result;
    }
    /**
     * @brief Get block of data
     */
    ull *gbl(int idx) { return blocks[idx]; }

    /**
     * @brief write blocks to output file
     */
    void wb(ofstream &outpt)
    {
        ull carry = 0;
        int carry_bits = 0;
        for (int i = 0; i < block_count; i++)
        {
            for (int j = 0; j < BLOCK_SIZE; j++)
            {
                int bits = BLOCK_SIZE;
                while (bits > 0)
                {
                    int get_bits = min(8 - carry_bits, bits);
                    ull mask = (1ULL << get_bits) - 1;
                    ull masked = blocks[i][j] >> (bits - get_bits) & mask;
                    carry |= masked << (8 - carry_bits - get_bits);
                    carry_bits += get_bits;
                    bits -= get_bits;

                    if (carry_bits == 8)
                    {
                        outpt.put(carry);
                        carry = 0;
                        carry_bits = 0;
                    }
                }
            }
        }
        if (carry_bits > 0) outpt.put(carry);
    }
};

#ifdef DEV
void decrypt(ull block[], string password)
{
    int rep = l(BLOCK_SIZE * 2, password.length()) * REPETITIONS;

    for (int i = rep - 1; i >= 0; i--)
    {
        x(block, password[i % password.length()], i / 2);

        if (i & 1) v(block, password[i % password.length()], i / 2, true);
        else h(block, password[i % password.length()], i / 2, true);
    }
}

void erase_line()
{
    cout << "\r                                                                "
            "                 \r";
}

void logTime(bool force = false)
{
    static auto start = chrono::high_resolution_clock::now();
    static int count = 0;
    static int old = 0;
    static bool first = true;

    auto elapsed = chrono::high_resolution_clock::now() - start;
    if (force)
    {
        erase_line();
        cout << "PROGRESS: " << old << " PASSWORDS/SECOND";
    }
    if (first || elapsed > chrono::seconds(1))
    {
        erase_line();
        cout << "PROGRESS: " << count << " PASSWORDS/SECOND";
        start = chrono::high_resolution_clock::now();
        old = count;
        count = 0;
    }
    if (!first) count++;
    first = false;
}

void brute()
{
    ifstream inpt = gi("Enter file to decrypt");
    ifstream pass_list = gi("Enter password list");
    cout << endl;

    stringstream final("cuhk24ctf{");

    bio reader1(final);
    ull *expected = reader1.gbl(0);

    ull *block;
    bio reader2(inpt);
    block = reader2.gbl(0);

    logTime();
    string password;
    while (getline(pass_list, password))
    {
        if (!password.empty() && password.back() == '\r') password.pop_back();
        if (password.length() < 8) continue;
        ull temp[BLOCK_SIZE];
        memcpy(temp, block, sizeof(ull) * BLOCK_SIZE);
        decrypt(temp, password);

        if (arrcmp(temp, expected))
        {
            erase_line();
            cout << "Password found: " << password << endl;
            logTime(true);
        }
        else logTime();
    }
    erase_line();
    cout << "Completed." << endl;
}
#endif

#ifdef DEV
void m(bool encrypt = true)
#else
void m()
#endif
{
    ifstream inpt = gi("Enter file to encrypt");
    string password = gp();
    ofstream outpt = go();

    ull *block;
    bio reader(inpt);
    for (int i = 0; i < reader.gbc(); i++)
    {
        block = reader.gbl(i);
#ifdef DEV
        if (encrypt) e(block, password);
        else decrypt(block, password);
#else
        e(block, password);
#endif
    }
    reader.wb(outpt);
}

int main()
{
#ifdef DEV
    if (freopen("../devin.txt", "r", stdin) == NULL)
    {
        cerr << "Error: freopen() failed" << endl;
        return 1;
    }
    m();
    m(false);
    brute();
#else
    m();
#endif
    return 0;
}