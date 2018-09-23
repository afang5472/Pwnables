input: python -c 'print ("read" + "\x00\x00\x00\x00")*(256/8)'        

Inside GDB:
1. break after menu print out
	b *0x555555555079

2. Alloc() with idx = 0, input = "read..." & random 16 bytes

3. Delete() with idx = 9

4. gc() since now refCount = 0 & theOBJ ptr != NULL; however, the theOBJ ptr has not been deleted
	by Delete() from Step #4, and it's still in the ArrayBuffer[0]

5. AllocOBJ() to spray the heap with objs full of "read..."

6. Now Use() to print out addr

--> leak binary addr

7. control rdata with addr of "write" to trigger arbitary write, this time with bigger probability to succeed!

8. write to ArrayBuffer[idx] to pretend that there's a gadget? then gc? -> needs arbitary write

9. leak libc addr

10. overwrite _free_hook variable in libc with fixed offset. This is the variable checked by libc before calling free(), and usually its NULL. Now with _free_hook = system() addr and with appropriate
		variable such as "/bin/sh" we can spawn shell
