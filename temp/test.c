#include<stdio.h>
#include<stdlib.h>
#include<string.h>
#include<unistd.h>
#include<fcntl.h>

//author : afang
//comment: what a nice day, isn't it?!

int main(){

	char *envp[] = {NULL};
	char *argv[] = {"a"};
	execve("/bin/ls", argv, envp);
	return 0;
}

