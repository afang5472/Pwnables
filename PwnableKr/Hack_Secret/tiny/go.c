#include<stdio.h>
#include<stdlib.h>
#include<string.h>
#include<unistd.h>
#include<sys/types.h>

//author : afang
//comment: what a nice day, isn't it?!

void launch(char** stack);

asm(
		"launch:\n\t"
		"mov esp,[esp+4]\n\t"
		"pop eax\n\t"
		"pop edx\n\t"
		"mov edx,[edx]\n\t"
		"call edx\n\t"
   );
int main(int argc, char* argv[]){

	//print PID.
	int pid = (int)getpid();
	printf("%d\n", pid);
	getchar();
	launch(argv-1);
	return 0;
}

