#!/bin/bash -

# These are the packages we don't want to build yet:
nobuild=$(grep -v '^#' IGNORE)

# Keep going (not safe).  Comment out for a safe build.
#keepgoing=--keepgoing

rm -f */*.src.rpm

# If any extra SRPMS need to be considered, list them here.  Otherwise
# leave this empty.
srpms=""

for dir in *; do
    if ! echo "$nobuild" | grep -sq "^$dir\$"; then
	if [ -d $dir -a -f $dir/*.spec ]; then
		if ! rpmbuild -bs --define "_sourcedir $(pwd)/$dir" --define "_srcrpmdir $(pwd)/$dir" $dir/*.spec; then
		  echo "Failed to create a source RPM in directory $dir."
		  echo "If you want to ignore this directory, you should add"
		  echo "it to the IGNORE file in the top level directory."
		  exit 1
		fi
		srpms="$srpms $(pwd)/$dir/*.src.rpm"
	fi
    fi
done

smock/smock.pl \
  --arch=i386 \
  --arch=x86_64 \
  --distro=fedora-rawhide \
  --distro=fedora-10 \
  $keepgoing \
  $srpms
