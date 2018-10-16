#include<stdio.h>
#include<stdlib.h>
#include<string.h>
#include<unistd.h>
#include<fcntl.h>

//author : afang
//comment: what a nice day, isn't it?!

int main(){

	//compare instructions with __builtin_expect..
	int a = 1;
	if(a){
		printf("branch hit!\n");
	}else{
		printf("branch missed!\n");
	}
	return 0;
}

