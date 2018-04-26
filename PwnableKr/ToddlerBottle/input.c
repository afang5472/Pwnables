#include<stdio.h>
#include<stdlib.h>

int main(){

    char *argv[101] = {"/home/input2/input", [1...99]="A",NULL};
    argv['A'] = "\x00";
    argv['B'] = "\x20\x0a\x0d";
    execve("/home/input2/input", argv, NULL);
}
