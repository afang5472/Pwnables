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

unsigned int syscall_addr = 0x2aa6ffe7;

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
		char *envp[] = {NULL};
		execl(filename, "\xe7\xff\xa6\x2a", "A", "A", "A", "A", "A", "A", "A", "A", "A", "A", "A", "A", "A", "A", "A", "A", "A", "A", "A", "A", "A", "A", "A", "A", "A",  NULL, envp);
	}else{
		while(1){
		wait(&wait_status);
		char buffer_[16];
		memcpy(buffer_, strsignal(WSTOPSIG(wait_status)), 16);
		if (!memcmp(buffer_, "Unknown signal 0", 16)){
			printf("[*]Crash!\n");	
			exit(1);
		}
		printf("child got signal: %s\n", buffer_);
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
		
		if(flager == 0 && single == 0){
			puts("try setting regs..");
	
			//control to read in.
			regs.eax = 0x3; //read syscall.
			regs.ebx = 0;
			regs.ecx = regs.esp;
			regs.edx = 0x4;

			regs.eip = syscall_addr;
			single = 1;

			ptrace(PTRACE_SETREGS, child_pid, NULL, &regs); //test control eip.
			ptrace(PTRACE_GETREGS, child_pid, NULL, &regs); //show if last worked.
			printf("before read, eax: %lx\n", regs.eax);
			printf("before read, ebx: %lx\n", regs.ebx);
			printf("before read, ecx: %lx\n", regs.ecx);
			printf("before read, edx: %lx\n", regs.edx);
			printf("eip is now at: %lx\n", regs.eip);	

			puts("go?");
			getchar();
			getchar();
		}

		//Single Step going.
	if(flager == 1 && single == 1){

			printf("execution reach before open.\n");
			
			//Set new args.
			regs.eax = 0x5; //open syscall.
			regs.ebx = regs.esp;
			regs.ecx = 0;
			regs.eip = syscall_addr;
			ptrace(PTRACE_SETREGS, child_pid, NULL, &regs);
		}

	if(flager == 2 && single == 1){

			//Set new args.
			regs.ebx = regs.eax;
			regs.eax = 0x3; //read syscall.
			regs.ecx = regs.esp;
			regs.edx = 0x50;
			regs.eip = syscall_addr;
			ptrace(PTRACE_SETREGS, child_pid, NULL, &regs);
		}

	if(flager == 3 && single == 1){

			//Set new args.
			regs.eax = 0x4; //write syscall.
			regs.ebx = 0x1;
			regs.ecx = regs.esp;
			regs.edx = 0x50;
			regs.eip = syscall_addr;
			ptrace(PTRACE_SETREGS, child_pid, NULL, &regs);
		}

		ptrace(PTRACE_SINGLESTEP, child_pid, NULL, NULL);
		
/*
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
        */	
	}

	}
	return 0;
}
