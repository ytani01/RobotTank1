#!/bin/sh

VENVDIR=$HOME/env2-robottank
BINDIR=$VENVDIR/bin
TOPDIR=$VENVDIR/RobotTank1
WORKDIR=$TOPDIR/Bt8BitDoZero2

cd $WORKDIR
while true; do
    . $BINDIR/activate
    echo "VIRTUAL_ENV=$VIRTUAL_ENV"

    python3 -m bt8bitdozero2 robottank 1

    deactivate

    echo -----
    sleep 2
done
