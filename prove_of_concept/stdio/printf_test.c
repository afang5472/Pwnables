#include<stdio.h>
#include<stdlib.h>
#include<string.h>

//author : afang
//comment: what a nice day, isn't it?!

int main(){

	size_t *ptr = (unsigned long*)&malloc;
	size_t *libc= (size_t)ptr - 0x97070; 
	printf("%p\n", libc);
	char *buffer = malloc(0x1000000);
	memset(buffer, 0x61, 0x1000000);
	*(size_t *)((size_t)libc + 0x3ebc30) = 0x1;
	fprintf(stdout, "gogogo: %s\n", buffer);
	return 0;
}

