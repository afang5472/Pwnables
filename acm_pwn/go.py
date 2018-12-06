#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# Auth0r : afang
# nice day mua! :P
# desc:

#lambs:
wait = lambda x: raw_input(x)

# imports

from binaryfang import *
import time
import os
import sys

elf = ""
libc = ""
env = ""
LOCAL = 1
context.log_level = "debug"



#round x

def create_str(content):

    p.sendline("1")
    time.sleep(0.1)
    p.sendline(content)

def sort():

    p.sendline("2")
    return p.recv()

while 1:

    for i in range(10,100):

        p = process("./acm")
        p.sendline("9000") #Init rounds.
        for j in range(i):
            
            create_str("a" * 100 * (i - j + 1))
            pause()
            sort()
            pause()
    try:
        for x in range(10):
            sort()
        p.close()
    except:
        print i
        print "critical"
        wait('now')
            


