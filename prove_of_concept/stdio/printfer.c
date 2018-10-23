#include<stdio.h>
#include<stdlib.h>
#include<string.h>

//author : afang
//comment: what a nice day, isn't it?!

int main(){

	char p[8];
	size_t *ptr = (unsigned long*)&malloc;
	size_t *libc= (size_t)ptr - 0x97070; 
	printf("%p\n", libc);
	char *buffer = malloc(0x1000000);
	strcpy(buffer, "%100000s");
	*(size_t *)((size_t)libc + 0x3ebc30) = 0x1;
	printf(buffer, &p);
	return 0;
}

