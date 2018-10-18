#include<stdio.h>
#include<stdlib.h>
#include<string.h>
#include<unistd.h>
#include<fcntl.h>

//author : afang
//comment: what a nice day, isn't it?!

struct A{

	int fd;
	char x[40];
};

struct B{

	struct A test;
	size_t x;

};

int main(){

	struct A x;
	struct B y;
	printf("size of A: %d\n", sizeof(x));
	printf("size of B: %d\n", sizeof(y));
	return 0;
}

