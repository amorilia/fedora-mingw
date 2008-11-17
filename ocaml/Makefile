# -*- Makefile -*-
# Test programs for testing out the cross-compiler.

all: test1 test1.exe test2 test2.exe test3 test3.exe test4 test4.exe \
	test_format test_format.exe sudoku sudoku.exe \
	test_buffer test_buffer.exe test_overflow test_overflow.exe \
	test_float test_float.exe test_float2 test_float2.exe

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

test_format: test_format.ml
	ocamlopt $< -o $@

test_format.exe: test_format.ml
	i686-pc-mingw32-ocamlopt $< -o $@

sudoku: sudoku.ml
	ocamlopt $< -o $@

sudoku.exe: sudoku.ml
	i686-pc-mingw32-ocamlopt $< -o $@

test_buffer: test_buffer.ml
	ocamlopt $< -o $@

test_buffer.exe: test_buffer.ml
	i686-pc-mingw32-ocamlopt $< -o $@

test_overflow: test_overflow.ml
	ocamlopt $< -o $@

test_overflow.exe: test_overflow.ml
	i686-pc-mingw32-ocamlopt $< -o $@

test_float: test_float.ml
	ocamlopt $< -o $@

test_float.exe: test_float.ml
	i686-pc-mingw32-ocamlopt $< -o $@

test_float2: test_float2.ml
	ocamlopt $< -o $@

test_float2.exe: test_float2.ml
	i686-pc-mingw32-ocamlopt $< -o $@

clean:
	rm -f test[1-4] test_format sudoku test_buffer test_overflow \
	  test_float test_float2 \
	  *.exe *.cmi *.cmx *.o
