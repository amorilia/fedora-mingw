#!/bin/sh -

# mingw64-scripts
# Copyright (C) 2008 Red Hat Inc., Richard W.M. Jones.
# Copyright (C) 2008 Levente Farkas
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

# This is a useful command-line script through which one can use the
# macros from mingw64-macros.mingw64 cross-compilation. 

NAME="_`basename $0|tr -- - _`"
eval "`rpm --eval "%{$NAME}"`" "$@"
