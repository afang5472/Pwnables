#include<stdio.h>
#include<stdlib.h>
#include<string.h>
#include<unistd.h>
#include<fcntl.h>

//author : afang
//comment: what a nice day, isn't it?!

struct struct_name{

	char a[50];
	long test;	
};

int main(){

	struct struct_name go1;
	printf("%d", sizeof(go1));

	return 0;
}

