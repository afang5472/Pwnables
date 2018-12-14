#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# Auth0r : afang
# nice day mua! :P
# desc:

#lambs:
wait = lambda x: raw_input(x)

# imports

fp = open("./subl" , "rb")

content = fp.read()

binary = content[0x4e60: 0x14e60]

fp2 = open("bin", "wb")

fp2.write(binary)
fp2.close()
