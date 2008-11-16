# -*- Makefile -*-
# Test programs for ocaml-calendar.

OCAMLOPTFLAGS = str.cmxa unix.cmxa -I +calendar calendarLib.cmx

SRCS = gen_test.ml test_fcalendar.ml test_time.ml test_calendar.ml \
  test_fpcalendar.ml test_pcalendar.ml test_timezone.ml test_date.ml \
  test_ftime.ml test_printer.ml test.ml

all: test test.exe

test: $(SRCS)
	ocamlopt $(OCAMLOPTFLAGS) $^ -o $@

test.exe: $(SRCS)
	i686-pc-mingw32-ocamlopt $(OCAMLOPTFLAGS) $^ -o $@

clean:
	rm -f test *.exe *.cmi *.cmx *.o
