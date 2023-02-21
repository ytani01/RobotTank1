#!/bin/sh

VENVDIR=$HOME/env2-robottank
BINDIR=$VENVDIR/bin
TOPDIR=$VENVDIR/RobotTank1
WORKDIR=$TOPDIR/Bt8BitDoZero2

MTR_HOST=localhost
MTR_PORT=12345
#DEV=1
DEV=0

cd $WORKDIR
while true; do
    . $BINDIR/activate
    echo "VIRTUAL_ENV=$VIRTUAL_ENV"

    python3 -m bt8bitdozero2 robottank -s $MTR_HOST -p $MTR_PORT $DEV

    deactivate

    echo -----
    sleep 2
done
