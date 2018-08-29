#include<stdio.h>
#include<stdlib.h>
#include<string.h>
#include<unistd.h>
#include<sys/syscall.h>
#include<sys/reg.h>
#include<sys/wait.h>
#include<sys/user.h>
#include<sys/ptrace.h>

//author : afang
//comment: what a nice day, isn't it?!

int main(int argc, char *argv[]){

	char *filename = argv[1];
	struct user_regs_struct regs;
	int wait_status;
	int flager = 0;
	int switcher = 0;
	
	pid_t child_pid = fork();
	if(child_pid == 0){
	/*	if(ptrace(PTRACE_TRACEME, 0, 0, 0) < 0) {
			perror("ptrace failed.");
			return;
		} */
		sleep(2);
		execve(filename, NULL, NULL);
	}else{
		while(1){
		wait(&wait_status);
		printf("child got signal: %s\n", strsignal(WSTOPSIG(wait_status)));
		printf("sig number: %lx\n", wait_status);
		ptrace(PTRACE_GETREGS, child_pid, NULL, &regs); //inspect registers.
		printf("eip at %lx\n", regs.eip);
		printf("eax is %lx\n", regs.eax);
		printf("ebx is %lx\n", regs.ebx);
		printf("ecx is %lx\n", regs.ebx);
		printf("edx is %lx\n", regs.ebx);
		printf("esp is %lx\n", regs.esp);
		puts("g? ------------- ");
		scanf("%d", &flager);
		getchar();
		
		if(flager == 1 && switcher == 0){
			puts("try setting regs..");
			//set regs and memory to execve.
	
			ptrace(PTRACE_POKETEXT, child_pid, 0x8048090, 0x80cd); //int 0x80
			ptrace(PTRACE_POKETEXT, child_pid, 0x80480a0, 0x6e69622f);//bin/sh
			ptrace(PTRACE_POKETEXT, child_pid, 0x80480a0 + 4, 0x0068732f);//bin/sh


			//control to execve.
			regs.eax = 0xb;
			regs.ebx = 0x80480a0;
			regs.ecx = 0;
			regs.edx = 0;
			regs.eip = 0x8048090;

			ptrace(PTRACE_SETREGS, child_pid, NULL, &regs); //test control eip.
			ptrace(PTRACE_GETREGS, child_pid, NULL, &regs); //show if last worked.
			printf("before execve, eax: %lx\n", regs.eax);
			printf("before execve, ebx: %lx\n", regs.ebx);
			printf("before execve, ecx: %lx\n", regs.ecx);
			printf("before execve, edx: %lx\n", regs.edx);
			printf("eip is now at: %lx\n", regs.eip);	
			puts("go?");
			getchar();
	}
		if(flager != 1){
			ptrace(PTRACE_SINGLESTEP, child_pid, NULL, NULL); //single step move on
		}else{
			switcher = 1;
			ptrace(PTRACE_CONT, child_pid, NULL, NULL);
		}
	}
	}
	return 0;
}
