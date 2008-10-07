#!/bin/sh -

PORT=22222
SERVER=annexia.org
USERNAME=rich
REMOTEDIR=tmp/mingw/

rsync -av --delete \
  ~/public_html/smock/yum/fedora-9 \
  -e "ssh -p $PORT" \
  $USERNAME@$SERVER:$REMOTEDIR
