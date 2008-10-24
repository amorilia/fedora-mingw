# Build some Cairo/Gtk test programs under Wine.

CFLAGS	= -g `pkg-config --cflags gtk+-2.0`
LIBS	= `pkg-config --libs gtk+-2.0`

MINGW32_LIBDIR=/usr/i686-pc-mingw32/sys-root/mingw/lib

all: svgspacewar svgspacewar.exe

svgspacewar: svgspacewar.c
	gcc $(CFLAGS) $< $(LIBS) -o $@

svgspacewar.exe: svgspacewar.c
	export PKG_CONFIG_PATH=$(MINGW32_LIBDIR)/pkgconfig; \
	i686-pc-mingw32-gcc $(CFLAGS) $< $(LIBS) -o $@

clean:
	rm -f svgspacewar svgspacewar.exe *~
