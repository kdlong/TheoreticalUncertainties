#!/bin/bash

echo "Command must be run from a clean environment! (i.e. no cmsenv)"
cern-get-sso-cookie -u https://cms-pdmv-dev.cern.ch/mcm/ -o ~/private/cookie.txt --krb -r 
cern-get-sso-cookie -u https://cms-pdmv.cern.ch/mcm/ -o ~/private/prod-cookie.txt --krb -r
cern-get-sso-cookie -u https://cms-pdmv-int.cern.ch/mcm/ -o ~/private/int-cookie.txt --krb -r 
cern-get-sso-cookie -u https://cms-pdmv-dev.cern.ch/mcm/ -o ~/private/dev-cookie.txt --krb -r

