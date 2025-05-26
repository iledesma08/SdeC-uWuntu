CC=gcc
CFLAGS=-Wall -Wextra -O2
PREFIX=/usr/local
BINDIR=$(PREFIX)/bin

hello: hello.c
	$(CC) $(CFLAGS) -o hello hello.c

install: hello
	install -d $(BINDIR)
	install -m 755 hello $(BINDIR)/hello

clean:
	rm -f hello

.PHONY: install clean