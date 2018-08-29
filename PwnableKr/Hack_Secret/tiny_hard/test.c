#include<stdio.h>
#include<stdlib.h>
#include<string.h>
#include<unistd.h>
#include<sys/syscall.h>

//author : afang
//comment: what a nice day, isn't it?!

int main(){

	
	getchar();
	char buffer[20];
	memcpy(buffer, "/bin/sh", 0x10);
	return 0;
}

