#include<stdio.h>
#include<unistd.h>
#include<sys/ptrace.h>
#include<sys/wait.h>
#include<stdlib.h>

pid_t checkpoint();
void resume_from_checkpoint(pid_t pid);

int main(int argc, char *argv[]){

	int i;
	pid_t child_pid;
	pid_t parent_pid = getpid();
	//printf("parent_Pid: %d", parent_pid);
	for(i=0; i<10; i++){
		if(i==4){
			printf("%6s: Checkpointing!\n", (getpid() == parent_pid));
			child_pid = checkpoint();
		}

		if(i==7 && (getpid()==parent_pid)){
			printf("%6s: Restarting!\n", (getpid() == parent_pid));
			resume_from_checkpoint(child_pid);
		}

		printf("%6s: i = %d\n", (getpid() == parent_pid)? "parent":"child", i);
	}
	return 0;
}

pid_t checkpoint(){

	pid_t pid;
	int wait_val;

	switch(pid=fork()){

		case -1:
			perror("fork");
			break;
		case 0:
			ptrace(PTRACE_TRACEME, 0,0,0);
			raise(SIGTRAP);
			break;
		default:
			wait(&wait_val);
			return pid;
	}	
}

void resume_from_checkpoint(pid_t pid){

	ptrace(PTRACE_CONT, pid, NULL, NULL);
	ptrace(PTRACE_DETACH, pid, NULL, NULL);
	exit(1);
}
