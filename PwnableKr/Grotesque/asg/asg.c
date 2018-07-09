#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <sys/mman.h>
#include <seccomp.h>
#include <sys/prctl.h>
#include <fcntl.h>
#include <sys/socket.h>
#include <unistd.h>

#define LENGTH 128

void sandbox(){
	scmp_filter_ctx ctx = seccomp_init(SCMP_ACT_KILL);
	if (ctx == NULL) {
		printf("seccomp error\n");
		exit(0);
	}

	seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(open), 0);
	seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(read), 0);
	seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(write), 0);
	seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(exit), 0);
	seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(exit_group), 0);

	if (seccomp_load(ctx) < 0){
		seccomp_release(ctx);
		printf("seccomp error\n");
		exit(0);
	}
	seccomp_release(ctx);
}

void shuffle(char *array, size_t n){
	int i, j;
	char t;
	for(i = 0; i < n - 1; i++){
		j = rand() % n;
		t = array[j];
		array[j] = array[i];
		array[i] = t;
	}
}

char *rand_string(char *str, size_t size){
	const char charset[] = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789";
	size_t n;
	int key;
	if(size){
		--size;
		for (n = 0; n < size; n++){
			key = rand() % (int) (sizeof charset - 1);
			str[n] = charset[key];
		}
		str[size] = '\0';
	}
	return str;
}

char stub[] = "\x48\x31\xc0\x48\x31\xdb\x48\x31\xc9\x48\x31\xd2\x48\x31\xf6\x48\x31\xff\x48\x31\xed\x4d\x31\xc0\x4d\x31\xc9\x4d\x31\xd2\x4d\x31\xdb\x4d\x31\xe4\x4d\x31\xed\x4d\x31\xf6\x4d\x31\xff";
unsigned char filter[256];
int main(int argc, char* argv[]){

	setvbuf(stdout, 0, _IONBF, 0);
	setvbuf(stdin, 0, _IOLBF, 0);

	printf("Welcome to Automatic Shellcode Generation (ASG) challenge\n");
	printf("your mission is making an arbitrary-file-reading shellcode\n");
	printf("but, can you make this with randomly given set of bytes?\n");
	sleep(5);
	getchar();

	int fd = open("/dev/urandom", O_RDONLY);
	int seed;
	read(fd, &seed, 4);
	srand(seed);

	int i;
	for(i=0; i<256; i++) filter[i] = i;
	shuffle(filter, 256);
	printf("these are filtered set of bytes:\n");
	write(1, filter, LENGTH);

	FILE *fp;
	int state;
	char filename[128];
	// you don't have permission to read this binary. don't bother.
	fp = popen("./genflag", "r");
	if(fp==NULL || fgets(filename, 128, fp)==NULL){
		printf("challenge broken. tell admin\n");
		exit(0);
	}
	filename[strlen(filename)-1] = 0;
	printf("flag is inside this file: [%s]\n", filename);

	unsigned char* sh = (char*)mmap(0, 0x1000, 7, MAP_ANONYMOUS | MAP_PRIVATE, 0, 0);
	memset(sh, 0x90, 0x1000);
	memcpy(sh, stub, strlen(stub));
	
	int offset = strlen(stub) + rand()%100;
	int r, j;
	printf("give me your shellcode: ");
	r = read(0, sh+offset, 1000);
	for(i=0; i<r; i++){
		for(j=0; j<LENGTH; j++){
			if(sh[offset+i] == filter[j]){
				printf("caught by filter!\n");
				exit(0);
			}
		}
	}

	sleep(10);
	alarm(10);
	if(shutdown(0, SHUT_RD)!=0){
		printf("shutdown error\n");
		exit(0);
	}
	if(chroot("/home/asg_pwn")!=0){	// this binary has cap_sys_chroot. symlink in /tmp will not work :p
		printf("chroot error\n");
		exit(0);
	}
	printf("buena suerte!\n");
	sandbox();
	alloca((rand()*12345) % 1024);
	asm("jmp *%0" :: "r"(sh));
	return 0;
}

