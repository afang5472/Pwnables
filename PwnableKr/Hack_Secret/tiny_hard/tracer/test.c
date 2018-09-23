#include<stdio.h>
#include<stdlib.h>
#include<string.h>
#include<unistd.h>
#include<fcntl.h>

//author : afang
//comment: what a nice day, isn't it?!

int main(){

	char *argv[] = {"AAAA", "bbbb", NULL};
	char *envp[] = {"NULL"};
	execve("./hack", argv, envp);
	return 0;
}

