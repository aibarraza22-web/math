CC = gcc
CFLAGS = -O3 -march=native -Wall

all: src/checker src/anneal

src/checker: src/checker.c
	$(CC) $(CFLAGS) -o $@ $<

src/anneal: src/anneal.c
	$(CC) $(CFLAGS) -o $@ $< -lm

clean:
	rm -f src/checker src/anneal
