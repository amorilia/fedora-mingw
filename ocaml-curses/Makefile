# -*- Makefile -*-
# Test programs.

all: test1 test1.exe

# XXX The native ocaml-curses package is broken ...
test1: test1.ml
#	ocamlfind ocamlopt -package curses $< -o $@
	ocamlopt -I +curses mlcurses.cmxa $< -o $@ -cclib -lncurses

# XXX ... and the META file for this package also doesn't work either.
test1.exe: test1.ml
#	OCAMLFIND_CONF=/etc/i686-pc-mingw32-ocamlfind.conf \
#	ocamlfind ocamlopt -package curses $< -o $@
	i686-pc-mingw32-ocamlopt -verbose -I +curses mlcurses.cmxa $< -o $@

clean:
	rm -f test1 \
	  *.exe *.cmi *.cmx *.o
