#!/bin/sh

VENVDIR=$HOME/env2-robottank
BINDIR=$VENVDIR/bin
TOPDIR=$VENVDIR/RobotTank1
WORKDIR=$TOPDIR/DcMtr

. $BINDIR/activate

echo "VIRTUAL_ENV=$VIRTUAL_ENV"

cd $WORKDIR
while true; do
    python3 -m dc_mtr dc-mtr-server 17 18 13 12 -p 12345
    sleep 2
done
