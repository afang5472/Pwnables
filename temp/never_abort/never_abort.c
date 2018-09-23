#include<stdio.h>
#include<stdlib.h>
#include<string.h>
#include<unistd.h>
#include<fcntl.h>
#include<signal.h>


//author : afang
//comment: what a nice day, isn't it?!

char secret[4]; 
void (*ret_addr)(char *, char**) = NULL;
char input[4];
char **argver = NULL;
char **envper = NULL;
char target[400];

void readin(char *buffer, long *count){

	char buf;
	int i = 0;
	for(i = 0; i < (unsigned long)(*count - 1); ++i){

		read(0, &buf, 1);
		if( buf == '\n' ){
			break;
		}
		*(buffer + i) = buf;
	}
	*(buffer + i) = '\x00';
	*(int*)(count) = i;
}


void handler(){

	register char **temp;
	int ans = 2;
	char content[4];
	char area[0x100];
	write(2, "[*]Signal handling process initialing..\n", 40);
	ret_addr = __builtin_return_address(0);
	printf("[*]you want to abort or what?Y/N: ");
	readin(content, &ans);
	if(*content == 'N'){
		exit(0);
	}
	memset(area, 0 , 0x100);
	readlink("/proc/self/exe", &area, 0xFF);
	puts("wait, give me your secret?? ");
	read(0, input, 4);
	if(strcmp(secret, input) != 0){
		puts("Emmm. You're not the right guy, please abort!");
		exit(-1);
	}
	temp = argver;
	execve(area, argver, envper);
	asm("leave");
	(*ret_addr)(area, temp);	
}

int main(int argc, char** argv, char **envp){

	int fd = open("/dev/urandom", O_RDONLY);
	read(fd, secret, 4);
	close(fd);
	
	argver = argv;
	envper = envp;
	setvbuf(stdin, 0, 2, 0);
	setvbuf(stdout, 0, 2, 0);
	setvbuf(stderr, 0, 2, 0);
	signal(6, handler);
	printf("Gimme your name: \n");
	long counter = 256;
	readin(&target, &counter);
	printf("challenge me: \n");
	long size = 0x1000;
	char small_buf[20];
	readin(small_buf, &size);
	return 0;
}

