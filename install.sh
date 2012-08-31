#!/bin/bash

platform=$(uname)
version=$(python --version 2>&1 | perl -n -e '/Python (\d\.\d)\.\d/ && print $1')

if [[ "$platform" == "Darwin" ]]; then
  dir=$HOME/Library/Python/"$version"/site-packages
elif [[ "$platform" == "Linux" ]]; then
  dir=$HOME/.local/lib/python"$version"/site-packages
fi

cp -R jsimutils "$dir"

echo "export PYTHONPATH=$dir" >> $HOME/.profile

exit 0
