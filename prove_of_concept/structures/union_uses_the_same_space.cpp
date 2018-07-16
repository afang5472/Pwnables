#include<iostream>
#include<stdio.h>
#include<stdlib.h>
#include<string.h>

//author : afang
//comment: what a nice day, isn't it?!

using namespace std;

enum struct T: char { END, INT, PLUS, MINUS, MUL, DIV, LP, RP, ID, ASSIGN, EXIT, UPLUS, STR, UMINUS};

class Token{

	char* checksum;
	char* str;

	union{
		int size;
		int value;
	};
	T type;
}*pToken;



int main(){

	return 0;
}

