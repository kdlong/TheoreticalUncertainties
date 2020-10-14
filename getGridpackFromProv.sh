#!/bin/bash

gridpack=$(edmProvDump $1 | grep -o "'/cvmfs.*\.tar.*'")

echo "Gridpack is $gridpack"
if [[ $# -gt 1 ]]; then
    tar xf ${gridpack:1:-1} ./mgbasedir/VERSION
    head -n2 mgbasedir/VERSION
fi
