#!/bin/bash

gridpack=$(edmProvDump $1 | grep -o "'/cvmfs.*\.tar.*'")

echo "Gridpack is $gridpack"
if [[ $# -gt 1 ]]; then
    tar xf ${gridpack:1:-1} gridpack_generation*.log 
    logfile=gridpack_generation_codegen.log
    if [[ ! -e "$logfile" ]]; then
        logfile=gridpack_generation.log
    fi
    echo "Looking for MadGraph version in file $logfile"
    grep "MG5_aMC_v" $logfile
    rm gridpack_generation*.log
fi
