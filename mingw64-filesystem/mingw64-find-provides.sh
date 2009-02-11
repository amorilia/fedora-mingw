#!/bin/bash

# This script reads filenames from STDIN and outputs any relevant provides
# information that needs to be included in the package.

if [ "$1" ]
then
   package_name="$1"
fi

[ -z "$OBJDUMP" ] && OBJDUMP=x86_64-pc-mingw32-objdump

filelist=`sed "s/['\"]/\\\&/g"`

dlls=$(echo $filelist | tr [:blank:] '\n' | grep '\.dll$')

for f in $dlls; do
    basename=`basename $f | tr [:upper:] [:lower:]`
    echo "mingw64($basename)"
done
