#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# Auth0r : afang
# nice day mua! :P
# desc:

#lambs:
wait = lambda x: raw_input(x)

# imports

import binascii
from pwn import *

#w = open("lst", "a+")

prefix = "\x7f\x00\x00"

for i in range(0x100):

    data = chr(i)
    f = prefix + data
    print f
    
