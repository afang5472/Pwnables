#include<stdio.h>
#include<stdlib.h>
#include<string.h>
#include<fcntl.h>

//author : afang
//comment: what a nice day, isn't it?!

int main(){

	FILE *fp = fopen("/etc/passwd","rb");
	char *buf= (char*)malloc(200);
	fgets(buf, 100, fp);
	printf("%s\n", buf);
	return 0;
}

