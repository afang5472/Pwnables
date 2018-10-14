#include<stdio.h>
#include<stdlib.h>
#include<string.h>
#include<unistd.h>
#include<sys/syscall.h>

//author : afang
//comment: what a nice day, isn't it?!

#define six 0x123456781234
#define four 0x12345678

int main(){

	printf("sizeof unsigned: %d\n", sizeof(unsigned));
	printf("sizeof defines 6byte integer: %d\n", sizeof(six));
	printf("sizeof defines 4byte integer: %d\n", sizeof(four));
	return 0;
}

