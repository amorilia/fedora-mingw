#!/bin/sh

for i in */*.spec
do
  module=`dirname $i`

  echo "------------------------------------------------------"
  echo "Compare $module"

  reference=$HOME/src/fedora/$module/devel/$module.spec
  if [ ! -f $reference ]
  then
      echo "Missing reference module $reference"
  else
    python compare.py $reference $i
  fi
  echo
done
