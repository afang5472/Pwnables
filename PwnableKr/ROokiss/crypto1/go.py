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

cookie = ''
def go(ID,password):
    p = remote("0", 9006)
    p.recvuntil("ID\n")
    p.sendline(ID)
    p.recvuntil("PW\n")
    p.sendline(password)
    p.recvuntil("(")
    data = p.recvuntil(")").rstrip(")")
    p.close()
    return data

data = go("admin", "g"*16)

for i in range(2,100):

    payload = "-" *  (15 - i%16) + "--" + cookie
    for k in '1234567890abcdefghijklmnopqrstuvwxyz-_':
        print k
        p0 = go(payload + k, '')
        p1 = go('-' * (15 - i%16), '')
        if p0[:len(payload + k)] == p1[:len(payload + k)]:
            cookie += k
            print cookie
            break
