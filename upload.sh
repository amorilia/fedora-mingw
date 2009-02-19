#!/bin/sh -

SERVER=web.merjis.com
USERNAME=rich
REMOTEDIR=public_html/mingw/
BWLIMIT="--bwlimit=40" ;# kilobytes per second

rsync -av --delete $BWLIMIT \
  ~/public_html/smock/yum/{fedora-10,fedora-rawhide} \
  $USERNAME@$SERVER:$REMOTEDIR
