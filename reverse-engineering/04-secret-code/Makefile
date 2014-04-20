.PHONY: all clean

CFLAGS=-Os -Wall -Werror -m32

all: main

main: blob.c strings.c main.c stage1.h
	gcc $(CFLAGS) main.c -o main
	strip main

blob.c: stage1.bin
	python python/binpack.py
strings.c:
	python python/strpack.py

stage1.bin: stage1.o
	objcopy -O binary -j .text stage1.o stage1.bin

stage1.o: stage1.c stage1.h
	gcc $(CFLAGS) -fPIC -c stage1.c -o stage1.o

clean:
	rm -f stage1.bin strings.c blob.c *.o main
