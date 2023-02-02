#!/bin/sh

VENVDIR=$HOME/env2-robottank
BINDIR=$VENVDIR/bin
TOPDIR=$VENVDIR/RobotTank1
WORKDIR=$TOPDIR/AbShutter

. $BINDIR/activate

echo "VIRTUAL_ENV=$VIRTUAL_ENV"

cd $WORKDIR
while true; do
    python3 -m ab_shutter dc-mtr 1 2
    echo -----
    sleep 2
done
