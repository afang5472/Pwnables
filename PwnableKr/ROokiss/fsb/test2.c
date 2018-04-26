#include<unistd.h>
int main()
{
        char * argv[ ]={"ls","-al","/etc/passwd",(char *)0};
        char * envp[ ]={"PATH=/bin",0};
        execve("/bin/ls",argv,envp);
}
