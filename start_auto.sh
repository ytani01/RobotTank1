#!/bin/sh

VENVDIR=$HOME/env2-robottank
BINDIR=$VENVDIR/bin
TOPDIR=$VENVDIR/RobotTank1
WORKDIR=$TOPDIR/DistanceVL53L0X

cd $WORKDIR
pwd
while true; do
    . $BINDIR/activate
    echo "VIRTUAL_ENV=$VIRTUAL_ENV"

    python3 -m distancevl53l0x robottankauto 0 1

    deactivate

    echo -----
    sleep 2
done
