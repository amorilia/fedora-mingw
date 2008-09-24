#!/bin/sh

if [ -z "$LOCALREPO" -o -z "$ARCHES" ]; then
    echo '$LOCALREPO must point to local repository'
    echo '$ARCHES must contain list of architectures to build'
    exit 1
fi

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

    if [ $? != 0 ]; then
       echo "Build failed, leaving logs in $LOCALREPO/scratch"
       exit 1
    fi
    mv $LOCALREPO/scratch/*.src.rpm $LOCALREPO/$DIST/src/SRPMS
    mv $LOCALREPO/scratch/*.rpm $LOCALREPO/$DIST/$ARCH/RPMS
    mv $LOCALREPO/scratch/*.log $LOCALREPO/$DIST/$ARCH/logs/$SRPM/
done

createrepos

