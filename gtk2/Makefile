# Build some Gtk test programs under Wine.

CFLAGS	= -g `pkg-config --cflags gtk+-2.0`
LIBS	= `pkg-config --libs gtk+-2.0`

MINGW32_LIBDIR=/usr/i686-pc-mingw32/sys-root/mingw/lib

all: test1 test1.exe test2 test2.exe test3 test3.exe

test1: test1.c
	gcc $(CFLAGS) $< $(LIBS) -o $@

test1.exe: test1.c
	export PKG_CONFIG_PATH=$(MINGW32_LIBDIR)/pkgconfig; \
	i686-pc-mingw32-gcc $(CFLAGS) $< $(LIBS) -o $@

test2: test2.c
	gcc $(CFLAGS) $< $(LIBS) -o $@

test2.exe: test2.c
	export PKG_CONFIG_PATH=$(MINGW32_LIBDIR)/pkgconfig; \
	i686-pc-mingw32-gcc $(CFLAGS) $< $(LIBS) -o $@

test3: test3.c
	gcc $(CFLAGS) $< $(LIBS) -o $@

test3.exe: test3.c
	export PKG_CONFIG_PATH=$(MINGW32_LIBDIR)/pkgconfig; \
	i686-pc-mingw32-gcc $(CFLAGS) $< $(LIBS) -o $@

clean:
	rm -f test1 test2 test3 *.exe *~
