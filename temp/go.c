// gcc -o go go.c -fPIC -pie -Wl,-z,now
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include <fcntl.h>

#define LONG unsigned long long

typedef struct _OBJ{
    char rdata[256];
    char* wdata;
    LONG length;
    char* type;
}OBJ, *POBJ;

char g_buf[16];

POBJ AllocOBJ(){
    POBJ res = (POBJ)malloc(sizeof(OBJ));
    memset(res, 0, sizeof(OBJ));
    res->type = "none";
    fread(&(res->rdata), 1, 256, stdin);
    res->wdata = g_buf;
    res->length = sizeof(g_buf);
    fread(res->wdata, 1, res->length, stdin);
    return res;
}

#define MAXOBJ 16
void* randomPadding;
POBJ theOBJ;
POBJ ArrayBuffer[MAXOBJ];
int refCount;

void gc(){
    if(refCount == 0 && theOBJ != NULL){
        free(theOBJ);
        free(randomPadding);
        theOBJ = NULL;
    }
}

void Delete(unsigned int idx){
    ArrayBuffer[idx] = NULL;
    refCount--;
}

void Alloc(unsigned int idx){
    unsigned int rlen;
    if(refCount==0){
        // According to some research papers, random-heap-padding mitigates heap exploits!
        rlen = abs((rand()*1228) % 1024); //0-1023
        randomPadding = malloc( rlen ); //malloc padding
        memset(randomPadding, 0xcc, rlen);
        theOBJ = AllocOBJ(); //a single OBJ.
    }
    ArrayBuffer[idx] = theOBJ;
    refCount++;
}

void Use(unsigned int idx){
    if(idx >= MAXOBJ){
        printf("[*]Error: Number[%d] is out of scope.\n", idx);
        return;
    }

    POBJ p = ArrayBuffer[idx];
    if(p==NULL){
        printf("[*]Error: Number[%d] is null\n", idx);
        return;
    }

    if(!strcmp(p->type, "binaryfang")){
        fwrite(&(p->rdata), 1, 256, stdout);
    }
    int n;
    if(!strcmp(p->type, "webfang")){
        printf("input what?");
        fread(p->wdata, 1, p->length, stdin);
    }
}

int main(){
    int fd = open("/dev/urandom", O_RDONLY);
    unsigned int seed;
    if(read(fd, &seed, 4)!=4){
        printf("error\n");
        return 0;
    }
    srand(seed);
    alarm(120);
    setvbuf(stdout, 0, _IONBF, 0);	
    setvbuf(stdin, 0, _IONBF, 0);

    int menu = 0;
    int idx = 0;
    while(1){
        printf("[*]menu\n");
        printf("- 1. : allocate\n");
        printf("- 2. : clean\n");
        printf("- 3. : utilize\n");
        printf("- 4. : gc\n");
        printf("- 5. : infinite\n");
        printf("> ");
		
        scanf("%d", &menu);
        getchar();	// eat newline

        switch(menu){
            case 1: 
                printf("index? ");
                scanf("%d", &idx);
                getchar();	// eat newline
                Alloc(idx);
                break;

            case 2: 
                printf("index? ");
                scanf("%d", &idx);
                getchar();	// eat newline
                Delete(idx);
                break;

            case 3: 
                printf("index? ");
                scanf("%d", &idx);
                getchar();	// eat newline
                Use(idx);
                break;

            case 4:
                gc();
                break;

            case 5:
                AllocOBJ();
                break;

            default:
                printf("byebye.\n");
                exit(0);
                break;
        }
    }
    return 0;
}


