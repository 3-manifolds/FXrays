CFLAGS = -O3 -funroll-loops

CC = gcc-3.2
#CC = gcc

tests: tests/test0 tests/test1 tests/test2 tests/magic5

tests/test0:  tests/test0.c FXrays.o FXrays.h
	$(CC) -g $(CFLAGS) -o tests/test0 -I. tests/test0.c FXrays.o  -static -lc

tests/test1:  tests/test1.c FXrays.o  FXrays.h
	$(CC) $(CFLAGS) -o tests/test1 -I. tests/test1.c FXrays.o  -static -lc

tests/test2:  tests/test2.c FXrays.o  FXrays.h
	$(CC) $(CFLAGS) -o tests/test2 -I. tests/test2.c FXrays.o  -static -lc

tests/magic5:  tests/magic5.c FXrays.o  FXrays.h
	$(CC) $(CFLAGS) -o tests/magic5 -I. tests/magic5.c FXrays.o  -static -lc

FXrays.o: FXrays.c FXrays.h

clean:
	-rm *.o *.so tests/test0 tests/test1 tests/test2 tests/magic5
