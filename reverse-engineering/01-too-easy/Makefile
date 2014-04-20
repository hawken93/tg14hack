CC=gcc
CFLAGS=-O3 -Wall -Werror -m32



all: main

clean:
	rm -f main

.PHONY: all clean strip

main: main.c
	$(CC) $(CFLAGS) $< -o $@
