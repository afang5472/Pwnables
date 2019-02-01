#!/usr/bin/python -u

from hashlib import sha256
import sys


while True:
    try:
        n = int(raw_input())
    except EOFError:
        exit(0)
    h = sha256()
    i = 0
    while i < n:
        bn = min(4096, n-i) #bn is the count of input characters..
        s = sys.stdin.read(bn)
        if len(s) == 0:
            raise EOFError
        h.update(s)
        i += len(s)
    print h.hexdigest()
