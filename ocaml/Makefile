# -*- Makefile -*-
# Test programs for testing out the cross-compiler.

all: test1 test1.exe

test1: test1.ml
	ocamlopt $< -o $@

test1.exe: test1.ml
	i686-pc-mingw32-ocamlopt $< -o $@
