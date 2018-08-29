#include<stdio.h>
#include<stdlib.h>
#include<string.h>
#include<unistd.h>
#include<sys/syscall.h>
#include<fcntl.h>
//author : afang
//comment: what a nice day, isn't it?!

int main(){

	int fd = open("./flag",O_RDONLY);
	char buffer[15];
	read(fd, buffer, 15);
	write(1, buffer, 15);
	return 0;
}

