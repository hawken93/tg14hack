#include <stdio.h>
// Indirectly needs: <malloc.h>
// Indirectly needs: <string.h>

#include "stage1.h"
#define BUFSIZE 100

void stage1(	// Functions
		size_t (*_fwrite)(const void*,size_t,size_t,FILE*),
		int (*_fflush)(FILE*),
		char *(*_fgets)(char*,int,FILE*),
		int (*_fprintf)(FILE*,const char*,...),
		int (*_strcmp)(const char*,const char*),
		void *(*_malloc)(size_t),
		void (*_free)(void*),
		size_t (*_strlen)(const char *),
		unsigned char *str,	// Encrypted string.. NO zero terminating
		unsigned char *strkey,	// key sequence
		int len,	// TOTAL length
		int count,	// number of strings
		FILE* _stdin,
		FILE* _stdout
		){

	char buf[BUFSIZE];
	char *strings[count];
	int i,j;

	// Decrypt string
	for(i=0;i<len;i++)
		str[i] ^=strkey[i];

	// malloc enough bytes and zero terminate
	for(j=0;j<count;j++){
		strings[j] = _malloc((len/count)+1);
		strings[j][len/count]=0;
	}

	// Deinterleave the string
	for(i=0;i<len;i+=count)
		for(j=0;j<count;j++)
			strings[j][i/6] = str[i+j];
	
	// Do our logic
	_fwrite(strings[0] /* Enter your pass: */, 27, 1, _stdout);
	_fflush(_stdout);
	_fgets(buf,BUFSIZE,_stdin);
	buf[_strlen(buf)-1]=0;

	if(_strcmp(buf, strings[4] /* Password */)==0){
		_fprintf(_stdout,strings[2] /* %s\n */, strings[4] /* Token */);
	} else {
		_fprintf(_stdout,strings[3] /* No-can-do */);
	}
	for(j=0;j<count;j++)
		_free(strings[j]);
}
