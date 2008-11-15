# -*- Makefile -*-
# Test programs for testing out the cross-compiler.

all: test1 test1.exe test2 test2.exe

test1: test1.ml
	ocamlopt $< -o $@

test2: test2.ml
	ocamlopt unix.cmxa $< -o $@

test1.exe: test1.ml
	i686-pc-mingw32-ocamlopt $< -o $@

test2.exe: test2.ml
	i686-pc-mingw32-ocamlopt unix.cmxa $< -o $@

clean:
	rm -f test1 test2 *.exe *.cmi *.cmx *.o
