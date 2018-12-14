#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# Auth0r : afang
# nice day mua! :P
# desc:

#lambs:
wait = lambda x: raw_input(x)

# imports
import sys

fp = open("./bin", "rb")

content = fp.read()

cnt = 0

for i in range(int(sys.argv[1])):

    temp1 = content[cnt:cnt+4][::-1].encode("hex")
    temp2 = content[cnt+4:cnt+8][::-1].encode("hex")
    temp3 = content[cnt+8:cnt+12][::-1].encode("hex")
    cnt += 12
    print temp1 + " ",
    print temp2 + " ",
    print temp3 + " "
