#include<stdio.h>
#include<stdlib.h>
#include<string.h>
#include<unistd.h>
#include<fcntl.h>

//author : afang
//comment: what a nice day, isn't it?!

int main(){

	//__builtin_expect indicates priority branch to be executed.
	int a = 1;
	if(__builtin_expect(a, 0)){
		printf("branch hit!\n");
	}else{
		printf("branch missed!\n");
	}
	return 0;
}

