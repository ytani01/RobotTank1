#!/bin/sh

VENVDIR=$HOME/env2-robottank
BINDIR=$VENVDIR/bin
TOPDIR=$VENVDIR/RobotTank1
WORKDIR=$TOPDIR/BtKbd

cd $WORKDIR
while true; do
    . $BINDIR/activate
    echo "VIRTUAL_ENV=$VIRTUAL_ENV"

    python3 -m btkbd robottank 1 2

    deactivate

    echo -----
    sleep 2
done
