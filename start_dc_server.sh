#!/bin/sh

VENVDIR=$HOME/env2-robottank
BINDIR=$VENVDIR/bin
TOPDIR=$VENVDIR/RobotTank1
WORKDIR=$TOPDIR/DcMtr

cd $WORKDIR
while true; do
    . $BINDIR/activate
    echo "VIRTUAL_ENV=$VIRTUAL_ENV"

    python3 -m dcmtr dc-mtr-server 17 18 13 12 -p 12345

    deactivate

    echo -----
    sleep 2
done
