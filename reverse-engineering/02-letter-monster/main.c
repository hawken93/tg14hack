#include <stdio.h>
#include <string.h>

#define BUFSIZE 100

#define TOKEN "M;+$i(|HFx<CFn}h"
// Super Duper Secret
// type ^ to get token
#define PASS "?a\\Q^k0a\\Q^k?QO^Q`"

unsigned char ascii_caesar(unsigned char c, int offset){
	const int start = 32;
	const int length = 95;

	// Not printable
	if(c < start || c >= (start+length)) return -1;
	
	// Make positive.. -1 = -1+95 = 94 (roll 94 right == 1 left)
	while(offset<0) offset += length;
	// Cap it
	offset = offset%length;
	// Roll c
	c = ((c-start+offset)%length)+start;

	return c;
}

void str_caesar(char *str, int off){
	int i;
	for(i=0;i<strlen(str);i++){
		str[i] = ascii_caesar(str[i], off);
	}
}

int main(){
	char buf[BUFSIZE];
	char pass[] = PASS;
	char token[] = TOKEN;
	// Read until newline

	fwrite("Enter the secret password: ", 27, 1, stdout);
	fflush(stdout);
	
	fgets(buf,BUFSIZE,stdin);
	buf[strlen(buf)-1]=0;
	str_caesar(buf,-93);
	str_caesar(pass,22);

	if(strcmp(buf,pass)==0){
		str_caesar(token,42);
		printf("Yay, your token is: %s\n", token);
	} else {
		printf("Wrong password!\n");
	}
	return 0;
}
