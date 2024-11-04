def get_flag_part():
    with open("flag.txt") as f:
        flag = f.read()
        assert len(flag) % 4 == 0
        step = len(flag) // 4
        flag_part = [flag[i:i+step] for i in range(0, len(flag), step)]
        return flag_part

def write_message(message, flag_part):
    with open("message.txt", "w") as f:
        f.write(message.format(flag1=flag_part[0], flag2=flag_part[1], flag3=flag_part[2], flag4=flag_part[3]))

def read_template():
    with open("message.md") as f:
        template = f.read()
        return template

write_message(read_template(), get_flag_part())
