#include<stdio.h>
#include<stdlib.h>
#include<string.h>
#include<unistd.h>
#include<sys/syscall.h>

//author : afang
//comment: what a nice day, isn't it?!

int main(){

	syscall(358, 0, NULL, NULL, NULL, 0x1000);
	return 0;
}

