with open("flags.txt") as f:
    lines = f.readlines()
    for line in lines:
        if len(line) != len(lines[0]):
            print(line)