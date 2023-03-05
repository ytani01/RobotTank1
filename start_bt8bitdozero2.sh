#!/bin/sh

VENVDIR=$HOME/env1-robot
BINDIR=$VENVDIR/bin
TOPDIR=$VENVDIR/RobotTank1
WORKDIR=$TOPDIR/Bt8BitDoZero2

MTR_HOST=localhost
MTR_PORT=12345
#DEV=1
DEV=0

. $BINDIR/activate
echo "VIRTUAL_ENV=$VIRTUAL_ENV"

cd $WORKDIR
pwd
while true; do
    if [ $# -gt 0 ]; then
        echo ----- pip install
        pip install .
    fi

    echo ----- bt8bitdozero2 robottank
    python3 -m bt8bitdozero2 robottank -s $MTR_HOST -p $MTR_PORT $DEV
    echo -----

    sleep 2
done
