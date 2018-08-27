#!/usr/bin/python -i

import capstone as cs

md=cs.Cs(cs.CS_ARCH_X86,cs.CS_MODE_32)

with open("vdso", "rb") as f:
    raw=f.read()

def get_instr_at(addr):
    d = md.disasm(raw[addr:addr+16], addr)
    try:
        return next(d)
    except StopIteration:
        return None

d={}
next_addr = {}
last_addr = {}

ds = {}
dsi = {}

for i in range(8192):
    inst = get_instr_at(i)
    if inst:
        d[i] = inst
        #if inst.mnemonic == 'jmp':
        next_addr[i] = i+inst.size
        ds[i] = inst.mnemonic + ' ' + inst.op_str

for x,y in next_addr.items():
    if y not in last_addr:
        last_addr[y]=set()
    last_addr[y].add(x)
for x,y in ds.items():
    if y not in dsi:
        dsi[y]=set()
    dsi[y].add(x)
#for i in d:
#    if d[i].bytes == '\\':
#        print i

def disasm(addr, n=128):
    if addr in last_addr:
        print 'Available last instructions:', last_addr[addr]
    else:
        print 'no last instruction available'
    for i in md.disasm(raw[addr:addr+n], addr):
        print ' '.join('{:02x}'.format(j) for j in i.bytes)
        print i.address, i.mnemonic, i.op_str
        
l = sorted(set(ds.values()))

for i in l:
    if 'esp' not in i: continue
    print i.ljust(60), '[', ', '.join(hex(j) for j in dsi[i]),']'

