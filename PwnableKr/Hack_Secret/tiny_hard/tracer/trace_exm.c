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
	int single = 0;
	
	pid_t child_pid = fork();
	if(child_pid == 0){
	/*	if(ptrace(PTRACE_TRACEME, 0, 0, 0) < 0) {
			perror("ptrace failed.");
			return;
		} */
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
		
		if(flager == 1 && single == 0){
			puts("try setting regs..");
			//set regs and memory to execve.
	
			ptrace(PTRACE_POKETEXT, child_pid, regs.esp, 0x6e69622f); //int 0x80
			ptrace(PTRACE_POKETEXT, child_pid, regs.esp + 4 , 0x68732f);//bin/sh

		
			//control to execve.
			regs.eax = 0xb;
			regs.ebx = 0x80bbc68;
			regs.ecx = 0;
			regs.edx = 0;

			puts("syscall?");
			unsigned int syscall_eip = 0;
			scanf("%u", &syscall_eip);
			regs.eip = syscall_eip + 0xfe7;
			single = 0;

			ptrace(PTRACE_SETREGS, child_pid, NULL, &regs); //test control eip.
			ptrace(PTRACE_GETREGS, child_pid, NULL, &regs); //show if last worked.
			printf("before execve, eax: %lx\n", regs.eax);
			printf("before execve, ebx: %lx\n", regs.ebx);
			printf("before execve, ecx: %lx\n", regs.ecx);
			printf("before execve, edx: %lx\n", regs.edx);
			printf("eip is now at: %lx\n", regs.eip);	

			unsigned int sh_text = ptrace(PTRACE_PEEKTEXT, child_pid, regs.esp ,NULL);
			printf("%d\n", sh_text);

			puts("go?");
			getchar();
			getchar();
		}
		if(single == 1 && flager==1){

			
			ptrace(PTRACE_GETREGS, child_pid, NULL, &regs); //show if last worked.
			regs.eax = 0xb;
			regs.ecx = 0;
			regs.edx = 0;
			ptrace(PTRACE_SETREGS, child_pid, NULL, &regs); //test control eip.
			ptrace(PTRACE_SINGLESTEP, child_pid, NULL, NULL); //single step move
			}
		if(flager ==0 || single == 0){
			ptrace(PTRACE_CONT, child_pid, NULL, NULL);
		}	
	}

	}
	return 0;
}
