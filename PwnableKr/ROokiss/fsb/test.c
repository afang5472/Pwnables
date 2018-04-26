#include<stdio.h>
#include<unistd.h>

int main(){

        char *p[] = {"./a.out"};
        execve("/bin/sh", 0, 0);
        return 0;
}
