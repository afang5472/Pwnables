#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# Auth0r : afang
# nice day mua! :P
# desc:

# imports

from pwn import *

context.log_level = "debug"

con = ssh(host='pwnable.kr', port = 2222, user = 'cmd3', password = 'FuN_w1th_5h3ll_v4riabl3s_haha')

p = con.remote("0",9023)

print p.recv()

