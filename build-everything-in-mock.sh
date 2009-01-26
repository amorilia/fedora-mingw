#!/bin/bash -

set -e

# These are the packages we don't want to build yet:
nobuild=$(grep -v '^#' IGNORE)

# Keep going - don't stop when smock hits an error.
keepgoing=--keepgoing

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

# Rawhide build everything:

smock/smock.pl \
  --arch=i386 \
  --arch=x86_64 \
  --distro=fedora-rawhide \
  $keepgoing \
  $srpms

# In Fedora 10 don't try to build the OCaml RPMs since they
# require OCaml 3.11 which was not in Fedora 10:

srpms_no_ocaml=""
for f in $srpms; do
    case $f in
    *ocaml* | *virt-top*) ;;
    *) srpms_no_ocaml="$srpms_no_ocaml $f" ;;
    esac
done

smock/smock.pl \
  --arch=i386 \
  --arch=x86_64 \
  --distro=fedora-10 \
  $keepgoing \
  $srpms_no_ocaml
