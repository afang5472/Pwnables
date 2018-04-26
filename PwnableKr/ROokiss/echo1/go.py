#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# Auth0r : afang
# nice day mua! :P
# desc:

# imports

from pwn import *

context.log_level = "debug"

p = process("./echo1")

print p.recvuntil("? : ")



