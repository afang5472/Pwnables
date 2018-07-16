#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# Auth0r : afang
# nice day mua! :P
# desc:

#lambs:
wait = lambda x: raw_input(x)

# imports

from binaryfang import *
import time
import os
import sys

elf = ""
libc = ""
env = ""
LOCAL = 1
context.log_level = "debug"

p = process("./acm")

p.sendline("8888") #Init rounds.

#round x

def create_str(content):

    p.sendline("1")
    time.sleep(0.1)
    p.sendline(content)

def sort():

    p.sendline("2")
    return p.recv()

for i in range(80):

    create_str("a" * (random.randint(100,500)))

pause()
print sort()
pause()
