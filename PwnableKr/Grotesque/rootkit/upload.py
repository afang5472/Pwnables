#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# Auth0r : afang
# nice day mua! :P
# desc:

# imports

from pwn import *
import time

f = open("./openat.b64","rb")

content = f.read()
print len(content)

#connecting to target 

context.log_level = 'debug'
p = ssh(user="rootkit",password="guest",host="pwnable.kr",port=2222)

time.sleep(20)

time.sleep(0.5)

print "let's begin."

p.run("id")
print p.recv()
