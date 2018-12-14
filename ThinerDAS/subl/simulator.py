#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# Auth0r : afang
# nice day mua! :P
# desc:

#lambs:
wait = lambda x: raw_input(x)

# imports

import os
import sys
from pwn import *

fp = open("./bin", "rb")

binary = fp.read()

print binary[:8].encode("hex")
