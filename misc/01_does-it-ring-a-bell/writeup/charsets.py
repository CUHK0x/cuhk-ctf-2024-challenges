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

# demostrate the charset
print('\n'.join([''.join(x) for x in possible_char]))

# write to a file for later usage
with open("choice.txt", "w") as f:
    f.write('\n'.join([''.join(x) for x in possible_char]))

# calculate possibilities from the 11th character to 31th character to verify that we can brute force within reasonable time
poss = 1
for arr in possible_char[10:]:
    poss *= len(arr)
print(poss)
