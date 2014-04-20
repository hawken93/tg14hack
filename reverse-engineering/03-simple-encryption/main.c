#include <stdio.h>
#include <string.h>

#include "strings.c"
#define BUFSIZE 100

// See python script for token and pass

void xor_string(unsigned char *str, unsigned char *str_key, unsigned int length){
	int i;
	for(i=0;i<length;i++)
		str[i] ^= str_key[i];
}

int main(){
	char buf[BUFSIZE];
	
	xor_string(token,token_key,token_len);
	xor_string(pass,pass_key,pass_len);

	fwrite("Enter the secret password: ", 27, 1, stdout);
	fflush(stdout);
	
	fgets(buf,BUFSIZE,stdin);
	buf[strlen(buf)-1]=0;

	if(strcmp(buf,(char *)token)==0){
		printf("Yay, your token is: %s\n", token);
	} else {
		printf("Wrong password!\n");
	}
	return 0;
}
