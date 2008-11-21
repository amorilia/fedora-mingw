#!/bin/sh -

PORT=22222
SERVER=annexia.org
USERNAME=rich
REMOTEDIR=tmp/mingw/
KBPS=25 ;# kilobytes per second

rsync -av --delete --bwlimit=$KBPS \
  ~/public_html/smock/yum/fedora-10 \
  -e "ssh -p $PORT" \
  $USERNAME@$SERVER:$REMOTEDIR
