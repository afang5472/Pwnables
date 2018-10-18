#include<stdio.h>
#include<stdlib.h>
#include<string.h>
#include<unistd.h>
#include<sys/syscall.h>

//author : afang
//comment: what a nice day, isn't it?!

int main(){

	char *temp = (char*)malloc(0xa8);
	char *padd = (char*)malloc(0xa8);
	scanf("%168s", temp);
	getchar();
	return 0;
}
