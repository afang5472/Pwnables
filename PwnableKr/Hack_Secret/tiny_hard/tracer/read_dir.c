#include<stdio.h>
#include<stdlib.h>
#include<string.h>
#include<unistd.h>
#include <sys/syscall.h>
#include<fcntl.h>

//author : afang
//comment: what a nice day, isn't it?!

int main(){


	char buf[0x1000];
	int fd = open("/home/flag_is_here", 0);
	syscall(141, fd, buf, 0x1000);
	getchar();

	return 0;
}

