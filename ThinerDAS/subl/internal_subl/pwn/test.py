#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# Auth0r : afang
# nice day mua! :P
# desc:

#lambs:
wait = lambda x: raw_input(x)

# imports

from pwn import *
context.log_level = "debug"

p = remote("124.16.75.162" , 40003)

data = p.recvuntil("> ")

p.interactive()
