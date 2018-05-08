#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# Auth0r : afang
# nice day mua! :P
# desc:

# imports
import sys

def if_ascii(input_str):

    for i in input_str:

        if ord(i) > 31 and ord(i) <= 127:
            continue
        else:
            return 0
    return 1

def get_input(filename):

    lst = []
    f = open(filename ,"rb")
    lines = f.readlines()
    for line in lines:
        if ':' in line:
            lst.append(line.strip())
    return lst

res = get_input(sys.argv[1])
seq = []
i = 0
for line in res:
    addr = line.split(":")[0].strip()
    if "0x" in addr:
        temp = addr[2:]
        t1 = temp[:2]
        print t1
        t2 = temp[2:4]
        t3 = temp[4:6]
        t4 = temp[6:]
        t = chr(int(t1,16)) + chr(int(t2,16)) + chr(int(t3,16)) + chr(int(t4,16))
        if if_ascii(t):
            seq.append(line)

w = open("filtered","wb")
for i in seq:

    w.write(i + "\n")

