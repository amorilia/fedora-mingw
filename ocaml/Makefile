# -*- Makefile -*-
# Test programs for testing out the cross-compiler.

all: test1 test1.exe test2 test2.exe test3 test3.exe test4 test4.exe

test1: test1.ml
	ocamlopt $< -o $@

test1.exe: test1.ml
	i686-pc-mingw32-ocamlopt $< -o $@

test2: test2.ml
	ocamlopt unix.cmxa $< -o $@

test2.exe: test2.ml
	i686-pc-mingw32-ocamlopt unix.cmxa $< -o $@

test3: test3.ml
	ocamlopt graphics.cmxa $< -o $@

test3.exe: test3.ml
	i686-pc-mingw32-ocamlopt graphics.cmxa $< -o $@

test4: test4.ml
	ocamlopt graphics.cmxa $< -o $@

test4.exe: test4.ml
	i686-pc-mingw32-ocamlopt graphics.cmxa $< -o $@

clean:
	rm -f test1 test2 test3 test4 *.exe *.cmi *.cmx *.o
