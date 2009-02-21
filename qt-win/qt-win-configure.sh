#!/bin/bash -

# Before running this, you will need the following RPMs installed:
#   . wine
#   . qt-devel
#   . mingw32-filesystem
# and you need to have downloaded the source zip file.  Run this
# command from the RPM SOURCES directory in order to (re-)create
# qt-win-configure.patch

# Notes:
#   . -no-mmx is needed because we didn't enable MMX instructions
#     when building GCC (I think?).  The error is:
#     /usr/lib64/gcc/i686-pc-mingw32/4.3.2/include/mmintrin.h:35:3:
#     error: #error "MMX instruction set not enabled"
#   . Same as above for -no-sse and -no-sse2

version=4.5.0-rc1
platform=fedora-win32-cross

set -e

if [ ! -f qt-win-opensource-src-$version.zip -o \
     ! -f qmake.conf -o \
     ! -f qplatformdefs.h ]; then
  echo "You're trying to run this from the wrong directory."
  echo "Run it from the RPM SOURCES directory, or Fedora CVS checkout."
  exit 1
fi

echo "Unpacking source file ... (this can take a minute or two)"

srcdir=qt-win-opensource-src-$version

rm -rf $srcdir.orig $srcdir

unzip -qq qt-win-opensource-src-$version.zip
cp -a $srcdir $srcdir.orig
mkdir $srcdir/mkspecs/fedora-win32-cross
cp qmake.conf qplatformdefs.h $srcdir/mkspecs/fedora-win32-cross

cd $srcdir

wine configure.exe \
  -platform $platform \
  -confirm-license \
  -no-qmake \
  -dont-process \
  -prefix $(rpm --eval %{_mingw32_prefix}) \
  -bindir $(rpm --eval %{_mingw32_bindir}) \
  -datadir $(rpm --eval %{_mingw32_datadir}) \
  -demosdir $(rpm --eval %{_mingw32_libdir})/qt4/demos \
  -docdir $(rpm --eval %{_mingw32_docdir}) \
  -examplesdir $(rpm --eval %{_mingw32_datadir})/qt4/examples \
  -headerdir $(rpm --eval %{_mingw32_includedir}) \
  -libdir $(rpm --eval %{_mingw32_libdir}) \
  -plugindir $(rpm --eval %{_mingw32_libdir})/qt4/plugins \
  -translationdir $(rpm --eval %{_mingw32_datadir})/qt4/translations \
  -no-mmx -no-sse -no-sse2 \
  -release \
  -shared > configure.output 2>&1

cd ..

rm -r $srcdir/mkspecs/fedora-win32-cross

diff -urN $srcdir.orig $srcdir > qt-win-configure.patch ||:

rm -r $srcdir.orig $srcdir

echo qt-win-configure.patch successfully updated