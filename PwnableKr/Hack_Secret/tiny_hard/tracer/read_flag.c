#include<stdio.h>
#include<stdlib.h>
#include<unistd.h>
#include<fcntl.h>

int main(){

	char buffer[20];
	read(0, buffer, 6);
	int fd = open(buffer, 0);
	printf("%d\n", fd);
	char content[30];
	read(fd, content, 30);
	write(1, content, 30);
	return 0;
}
