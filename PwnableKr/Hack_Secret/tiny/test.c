#include<stdio.h>
#include<stdlib.h>
#include<unistd.h>

//author : afang
//comment: what a nice day, isn't it?!

int main()
{
    char *envp[] = {
		"XXXX",
        NULL
    };
    execle("test", "AAAA",
			"BBBB", "C","C","C","C","C","C","C","C","C",NULL, envp);
    return 0;
}
