#!/bin/sh -

# mingw32-configure
# Copyright (C) 2008 Red Hat Inc., Richard W.M. Jones.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.

# This is a useful command-line script which configures
# a program for cross-compilation.  It is meant to be
# the equivalent of the %{_mingw32_configure} macro in
# /etc/rpm/macros.mingw32

mingw32_prefix=/usr/i686-pc-mingw32/sys-root/mingw
mingw32_libdir=$mingw32_prefix/lib
mingw32_host=i686-pc-mingw32
mingw32_target=i686-pc-mingw32
mingw32_cc=i686-pc-mingw32-gcc
mingw32_cflags="-O2 -g -pipe -Wall -Wp,-D_FORTIFY_SOURCE=2 -fexceptions --param=ssp-buffer-size=4"

PKG_CONFIG_PATH="$mingw32_libdir/pkgconfig" \
CC="$mingw32_cc" \
CFLAGS="$mingw32_cflags" \
./configure \
  --host=$mingw32_host \
  --target=$mingw32_target \
  --prefix=$_mingw32_prefix \
  "$@"
