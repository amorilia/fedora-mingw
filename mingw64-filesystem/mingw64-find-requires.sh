#!/bin/bash

# This script reads filenames from STDIN and outputs any relevant provides
# information that needs to be included in the package.

if [ "$1" ]
then
   package_name="$1"
fi

[ -z "$OBJDUMP" ] && OBJDUMP=x86_64-pc-mingw32-objdump

# Get the list of files.

filelist=`sed "s/['\"]/\\\&/g"`

# Everything requires mingw64-filesystem of at least the current version
# and mingw64-runtime.
echo 'mingw64-filesystem >= @VERSION@'
echo 'mingw64-runtime'

dlls=$(echo $filelist | tr [:blank:] '\n' | grep -Ei '\.(dll|exe)$')

for f in $dlls; do
    $OBJDUMP -p $f | grep 'DLL Name' | grep -Eo '[-._[:alnum:]]+\.dll' |
        tr [:upper:] [:lower:] |
        sed 's/\(.*\)/mingw64(\1)/'
done | sort -u
