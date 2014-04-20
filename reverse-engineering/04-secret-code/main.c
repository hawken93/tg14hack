#include <stdio.h>
#include <malloc.h>
#include <string.h>
#include <sys/mman.h>

#include "strings.c"
#include "blob.c"
#include "stage1.h"

int main(int argc, char **argv){
	int i;
	void (*_stage1)(
		size_t (*)(const void*,size_t,size_t,FILE*),
		int (*)(FILE*),
		char *(*)(char*,int,FILE*),
		int (*)(FILE*,const char*,...),
		int (*)(const char*,const char*),
		void *(*)(size_t),
		void (*)(void*),
		size_t (*)(const char *),
		unsigned char*,unsigned char*,int,int,FILE*,FILE*);
	char *exec;
	int mm_len = 4096; // We'll manualy limit ourselves to one page

	exec = mmap(0,mm_len, PROT_READ|PROT_WRITE|PROT_EXEC, MAP_PRIVATE|MAP_ANON, -1, 0);


	for(i=0;i<blob_len;i++){
		exec[i] = blob[i] ^ blob_key[i];
	}
	_stage1 = (void (*)(size_t (*)(const void*,size_t,size_t,FILE*),int (*)(FILE*),char *(*)(char*,int,FILE*),int (*)(FILE*,const char*,...),int (*)(const char*,const char*),void *(*)(size_t),void (*)(void*),size_t (*)(const char *),unsigned char*,unsigned char*,int,int,FILE*,FILE*)) exec;


	// Pass on str, strkey, len, count
	_stage1(fwrite,fflush,fgets,fprintf,strcmp,malloc,free,strlen,
			str,str_key,str_len,str_count,
			stdin,stdout);
	munmap(exec,4096);
	return 0;
}
