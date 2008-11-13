# Build some libcurl test programs under Wine.

CFLAGS = -g `pkg-config --cflags libcurl`
LIBS = `pkg-config --libs libcurl`

MINGW32_LIBDIR = /usr/i686-pc-mingw32/sys-root/mingw/lib

all: test1 test1.exe

test1: test1.c
	gcc $(CFLAGS) $< $(LIBS) -o $@

test1.exe: test1.c
	export PKG_CONFIG_PATH=$(MINGW32_LIBDIR)/pkgconfig; \
	i686-pc-mingw32-gcc $(CFLAGS) $< $(LIBS) -o $@

clean:
	rm -f test1 *.exe *~
