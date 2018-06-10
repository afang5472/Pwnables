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
import base64

elf = ""
libc = ""
env = ""
LOCAL = 1
context.log_level = "debug"


p = remote("pwnable.kr", 9005)


def getbin():
    time.sleep(0.2)
    p.recvuntil("wait...\n")

    data = p.recvuntil("here")
    binary = data.split("here")[0].strip()
    binary_file = open("binary_test2","wb")
    binary_file.write(base64.b64decode(binary))
    binary_file.close()
    
getbin()
