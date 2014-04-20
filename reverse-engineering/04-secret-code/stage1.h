void stage1(	size_t (*_fwrite)(const void*,size_t,size_t,FILE*),
		int (*_fflush)(FILE*),
		char *(*_fgets)(char*,int,FILE*),
		int (*_fprintf)(FILE*,const char*,...),
		int (*_strcmp)(const char*,const char*),
		void *(*_malloc)(size_t size),
		void (*_free)(void* ptr),
		size_t (*_strlen)(const char *),
		unsigned char *str,
		unsigned char *strkey,
		int len,
		int count,
		FILE* _stdin, FILE* _stdout);

