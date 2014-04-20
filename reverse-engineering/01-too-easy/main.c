#include <stdio.h>
#include <string.h>

#define TOKEN "23h2k2k2k2kddddRAWR"
#define PASS  "entotrefiire"
#define BUFSIZE 100

int check_password(const char *pw){
	if(strcmp(pw, PASS)==0) return 1;
	return 0;
}

int main(){
	char buf[BUFSIZE];
	// Read until newline
	fwrite("Enter the secret password: ", 27, 1, stdout);
	fflush(stdout);
	fgets(buf,BUFSIZE,stdin);
	buf[strlen(buf)-1]=0;
	if(check_password(buf)){
		printf("Yay, your token is: %s\n", TOKEN);
	} else {
		printf("Wrong password!\n");
	}
	return 0;
}
