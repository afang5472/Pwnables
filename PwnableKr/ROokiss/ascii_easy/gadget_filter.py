w = open("gadgets","r")
lines = w.readlines()
base_addr = 0x5555e000

def is_ascii(i):

    if i < 32 or i > 127:
        return 0
    return 1

def filter(addr):

    temp = hex(base_addr + addr)[2:]
    i = 0
    while i < 7:
        char = temp[i] + temp[i+1]
        i += 2
        if is_ascii(int(char,16)) == 0:
            return 0
    return 1

filtered = []
for line in lines:

    if line[0] == '0' and line[1] == 'x':
        line = line.strip("\n")
        if filter(int(line.split(":")[0].strip(),16)) == 1:
            filtered.append(line)

w = open("filtered","wb")
for line in filtered:
    w.write(line+"\n")
w.close()
    
