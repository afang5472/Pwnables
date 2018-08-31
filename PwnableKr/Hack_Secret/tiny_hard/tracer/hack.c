#include<stdio.h>
#include<stdlib.h>
#include<string.h>
#include<unistd.h>
#include<sys/syscall.h>
#include<sys/reg.h>
#include<sys/user.h>
#include<sys/ptrace.h>
#include<sys/wait.h>

//author : afang
//comment: what a nice day, isn't it?!

int main(){

	ptrace(PTRACE_TRACEME, 0,0,0);
	int a;
	scanf("%d", a);
	//raise(SIGSTOP);
	puts("reach here.");
	return 0;
}

