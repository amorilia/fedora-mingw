# Test some binaries which use ocaml-lablgl.  This builds both the
# Linux native and Windows binaries, so you can compare them.
#
# Note that the demos themselves are non-free, written by Jon Harrop
# and available from his website here:
# http://www.ffconsultancy.com/ocaml/

all: balls.opt balls.exe

%.opt: %.ml
	ocamlfind ocamlopt -I +lablGL unix.cmxa lablglut.cmxa lablgl.cmxa $< -o $@

%.exe: %.ml
	OCAMLFIND_CONF=/etc/i686-pc-mingw32-ocamlfind.conf \
	ocamlfind ocamlopt -I +lablGL unix.cmxa lablglut.cmxa lablgl.cmxa $< -o $@
