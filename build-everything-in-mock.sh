#!/bin/bash -

DIST=fedora-9
SKIP_BUILT_RPMS=1

LOCALREPO=$HOME/public_html/smock/yum
ARCHES="i386 x86_64"

export DIST SKIP_BUILT_SRPMS LOCALREPO ARCHES

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
    srcrpm=`rpmbuild --define "_sourcedir $pwd/$dir" -bs $spec`
    if [ $? != 0 ]; then exit 1; fi
    srcrpm=`echo $srcrpm | awk '{print $2}'`

    # Test if all the output RPMs exist already.
    skip=
    if [ $SKIP_BUILT_RPMS ]; then
	skip=1
	baserpm=`basename $srcrpm | sed 's/\.fc[[:digit:]]*\.src\.rpm//g'`
	for arch in $ARCHES; do
	    if [ ! -f $LOCALREPO/$DIST/$arch/RPMS/$baserpm.* ]; then
		skip=
	    fi
	done
    fi

    if [ $skip ]; then
	echo "skipping $srcrpm"
    else
	smock/smock.sh $DIST $srcrpm
    fi
done 2>&1 | tee -a buildall.log
