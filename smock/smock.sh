#!/bin/sh


LOCALREPO=$HOME/smock/yum
#ARCHES="i386 x86_64"
ARCHES=i386

help() {
    echo "syntax: $0 DIST SRPM"
}

if [ -z "$1" ]; then
    help
    exit
fi


if [ -z "$2" ]; then
    help
    exit
fi

DIST=$1
SRPM=$2

createrepos() {

  (
    mkdir -p $LOCALREPO/$DIST/src/SRPMS
    cd $LOCALREPO/$DIST/src
    rm -rf repodata
    createrepo .
  )

  for ARCH in $ARCHES
  do
    (
      mkdir -p $LOCALREPO/$DIST/$ARCH/RPMS
      mkdir -p $LOCALREPO/$DIST/$ARCH/logs
      cd $LOCALREPO/$DIST/$ARCH
      rm -rf repodata
      createrepo --exclude "logs/*rpm" .
    )
  done
}

createrepos

mkdir -p $LOCALREPO/scratch
rm -f $LOCALREPO/scratch/*

for ARCH in $ARCHES
do
    mkdir -p $LOCALREPO/$DIST/$ARCH/logs/$SRPM

    mock -r $DIST-$ARCH --resultdir $LOCALREPO/scratch $SRPM

    mv $LOCALREPO/scratch/*.src.rpm $LOCALREPO/$DIST/src/SRPMS
    mv $LOCALREPO/scratch/*.rpm $LOCALREPO/$DIST/$ARCH/RPMS
    mv $LOCALREPO/scratch/*.log $LOCALREPO/$DIST/$ARCH/logs/$SRPM/
done

createrepos
