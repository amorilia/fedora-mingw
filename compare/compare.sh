#!/bin/sh

for i in */*.spec
do
  module=`dirname $i`

  if [ "$module" == "portablexdr" ]; then continue ; fi
  if [ "$module" == "example" ]; then continue ; fi
  if [ "$module" == "filesystem" ]; then continue ; fi
  if [ "$module" == "iconv" ]; then continue ; fi
  if [ "$module" == "nsis" ]; then continue ; fi
  if [ "$module" == "runtime" ]; then continue ; fi
  if [ "$module" == "runtime-bootstrap" ]; then continue ; fi
  if [ "$module" == "w32api" ]; then continue ; fi
  if [ "$module" == "w32api-bootstrap" ]; then continue ; fi
  

  echo "------------------------------------------------------"
  echo "Compare $module"

  if [ "$module" == "gcc" ]; then
    reference=$HOME/src/fedora/$module/devel/gcc43.spec
  else
    reference=$HOME/src/fedora/$module/devel/$module.spec
  fi
  suppression=$module/compare.supp
  if [ ! -f $reference ]
  then
      echo "Missing reference module $reference"
  else
      python compare/compare.py $reference $i $suppression
  fi
  echo
done
