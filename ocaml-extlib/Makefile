# -*- Makefile -*-
# Test programs for extlib

OCAMLOPTFLAGS = -I +extlib extLib.cmxa

all: test1 test1.exe

test1: test1.ml
	ocamlopt $(OCAMLOPTFLAGS) $< -o $@

test1.exe: test1.ml
	i686-pc-mingw32-ocamlopt $(OCAMLOPTFLAGS) $< -o $@

clean:
	rm -f test1 *.exe *.cmi *.cmx *.o
