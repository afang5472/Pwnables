#include<stdio.h>
#include<stdlib.h>
#include<string.h>
#include<unistd.h>
#include<fcntl.h>

//author : afang
//comment: what a nice day, isn't it?!

void func(){

	int a;
	printf("etst.");
	scanf("%d", &a);
	return 0;
}



int main(){

	char *test = malloc(0xffffffffffffffff);
	printf("%p\n", test);
	func();
	return 0;
}

