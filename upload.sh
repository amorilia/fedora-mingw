#!/bin/sh -

PORT=22222
SERVER=annexia.org
USERNAME=rich
REMOTEDIR=tmp/mingw/
#BWLIMIT="--bwlimit=25" ;# kilobytes per second

rsync -av --delete $BWLIMIT \
  ~/public_html/smock/yum/{fedora-10,fedora-rawhide} \
  -e "ssh -p $PORT" \
  $USERNAME@$SERVER:$REMOTEDIR
