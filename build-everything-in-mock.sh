#!/bin/sh -

DIST=fedora-9

specs=`perl show-build-order.pl |
       grep -v '^#' |
       grep -Eo '[^[:space:]]+/mingw-[^[:space:]]+\.spec'`

rm -f buildall.log
echo -e "Specfiles in build order:\n$specs\n\n" >> buildall.log

pwd=`pwd`

for spec in $specs
do
    set -e
    dir=`dirname $spec`
    srcrpm=`rpmbuild --define "_sourcedir $pwd/$dir" -bs $spec |
            awk '{print $2}'`
    smock/smock $DIST $srcrpm
done 2>&1 | tee -a buildall.log
