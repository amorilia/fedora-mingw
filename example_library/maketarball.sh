#!/bin/sh
VERSION=1.0
rm -rf example-$VERSION/
mkdir example-$VERSION/
cp example.c example.h CMakeLists.txt runtest.c example-$VERSION/
tar cfvj ~/rpmbuild/SOURCES/example-$VERSION.tar.bz2 example-$VERSION/
rm -rf example-$VERSION/
