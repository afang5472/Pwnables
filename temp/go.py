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
import random

elf = ""
libc = ""
env = ""
LOCAL = 1
context.log_level = "debug"

p = process("./deathnote")

p.recvuntil("name:")

p.sendline("afang")

p.recvuntil(">>")
wait("me")

# overwrite read 
