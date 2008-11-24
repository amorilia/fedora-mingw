#!/bin/bash -

# These are the packages we don't want to build yet:
nobuild="example
cyrus-sasl
gdb
pidgin
python
nspr
nss
virt-ctrl
wix"

rm -f */*.src.rpm

for dir in *; do
    if ! echo "$nobuild" | grep -sq "^$dir\$"; then
	if [ -d $dir -a -f $dir/*.spec ]; then
	    (
		cd $dir
		rpmbuild -bs --define "_sourcedir $(pwd)" --define "_srcrpmdir $(pwd)" *.spec
	    )
	fi
    fi
done

smock/smock.pl --arch=i386 --arch=x86_64 --distro=fedora-10 */*.src.rpm
