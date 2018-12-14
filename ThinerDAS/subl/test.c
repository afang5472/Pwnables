#include<stdio.h>
#include<stdlib.h>
#include<string.h>
#include<sys/time.h>
//author : afang
//comment: what a nice day, isn't it?!

int main(){

	struct timeval  tv;
	gettimeofday(&tv, NULL);
	printf("%ld %ld\n", tv.tv_sec, tv.tv_usec);
	return 0;
}

