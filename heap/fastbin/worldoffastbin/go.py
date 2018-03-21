from pwn import *

context.log_level = "debug"

p = process("./fastbin")


def allocate(size, ):

    p.sendline("1")
    print p.recv()
    p.sendline(str(size))
    print p.recv()

def fill(index, size, content):

    p.sendline("2")
    print p.recv()
    p.sendline(index)
    print p.recv()
    p.sendline(str(size))
    print p.recv()
    p.send(content)
    print p.recv()

def free(index):

    p.sendline("3")
    print p.recv()
    p.sendline(index)
    print p.recv()

def dump(index):

    p.sendline("4")
    print p.recv()
    p.sendline(index)
    return p.recv()

allocate(0x20)
fill("0", 30, "a"*30)
print dump("0")
free("0")

