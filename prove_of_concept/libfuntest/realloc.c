#include "../depend.h"
//author : afang
//comment: what a nice day, isn't it?!

//testing for realloc features.
//ptr , size.


int main(){

//	printf("hello, test.\n");

	char *ptr = (char*)malloc(0x50);
	fprintf(stderr, "allocate at : %p\n", ptr);	
	realloc(ptr, 0);
	fprintf(stderr, "now, ptr is pointing at : %p\n", ptr);
	return 0;
}

