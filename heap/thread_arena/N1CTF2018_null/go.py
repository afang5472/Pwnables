from pwn import *
import time

context.log_level = "debug"

p = process("null")

passwd = "i'm ready for challenge"

print p.recv()

p.sendline(passwd)
time.sleep(2)
print p.recv()
