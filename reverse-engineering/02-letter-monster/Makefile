CC=gcc
CFLAGS=-Os -Wall -Werror -m32



all: main

strip:
	strip main

clean:
	rm -f main

.PHONY: all clean strip

main: main.c
	$(CC) $(CFLAGS) $< -o $@
