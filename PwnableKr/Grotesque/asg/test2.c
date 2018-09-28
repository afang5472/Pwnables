#include<stdio.h>
#include<stdlib.h>
#include<string.h>
#include<unistd.h>
#include<fcntl.h>
#include<sys/socket.h>

//author : afang
//comment: what a nice day, isn't it?!

int main(){

	setvbuf(stdout, 0, _IONBF, 0);
	setvbuf(stdin, 0, _IONBF, 0);
	char buf[51];
	read(0, buf, 50);
	printf("buf1: %s\n", buf);
	char buf2[51];
	int x = close(0);
	printf("ret: %d\n", x);
	read(0, buf2, 50);
	printf("buf2: %s\n", buf2);
	return 0;
}

