#include <sys/ptrace.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <unistd.h>
#include <sys/reg.h>   /* For constants ORIG_EAX etc */

int main()
{   pid_t child;
    long orig_eax;
    ptrace(PTRACE_TRACEME, 0, 0x12345678, NULL);
    execl("/bin/ls", "ls", NULL);
    wait(NULL);
    orig_eax = ptrace(PTRACE_PEEKUSER,
                          child, 4 * ORIG_EAX,
                          NULL);
    printf("The child made a "
               "system call %ld\n", orig_eax);
    ptrace(PTRACE_CONT, child, NULL, NULL);
    return 0;
}

