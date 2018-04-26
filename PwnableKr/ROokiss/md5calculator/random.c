#include<stdio.h>
#include<stdlib.h>
#include <assert.h>

int main(int argc, char *argv[]){

        assert(argc == 3);
        int timestamp = atoi(argv[1]);
        int captcha = atoi(argv[2]);
        srand(timestamp);
        int rands[8];
        for(int i = 0; i < 8; i++){
                rands[i] = rand();
        }
        int temp = rands[1] + rands[2] - rands[3] + rands[4] + rands[5] - rands[6] + rands[7];
        unsigned int res  = captcha - temp;
        printf("%d", res);
        return 0;
}
