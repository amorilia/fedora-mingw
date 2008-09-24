#!/bin/bash

# This script reads filenames from STDIN and outputs any relevant provides
# information that needs to be included in the package.

if [ "$1" ]
then
   package_name="$1"
fi

[ -z "$OBJDUMP" ] && OBJDUMP=i686-pc-mingw32-objdump

# Get the list of files.

filelist=`sed "s/['\"]/\\\&/g"`

# Everything requires mingw32-filesystem of at least the current version
# and mingw32-runtime.
echo 'mingw32-filesystem >= @VERSION@'
echo 'mingw32-runtime'

dlls=$(echo $filelist | tr [:blank:] '\n' | grep -Ei '\.(dll|exe)$')

for f in $dlls; do
    $OBJDUMP -p $f | grep 'DLL Name' | grep -Eo '[-._[:alnum:]]+\.dll' |
        tr [:upper:] [:lower:] |
        sed 's/\(.*\)/mingw32(\1)/'
done | sort -u
