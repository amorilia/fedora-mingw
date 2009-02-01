#!/bin/bash -

# Before running this, you will need the following RPMs installed:
#   . wine
#   . qt-devel
#   . mingw32-filesystem

wine configure.exe \
  -platform win32-g++ \
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
  -release \
  -shared
