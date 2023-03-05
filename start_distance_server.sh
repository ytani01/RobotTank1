#!/bin/sh

VENVDIR=$HOME/env1-robot
BINDIR=$VENVDIR/bin
TOPDIR=$VENVDIR/RobotTank1
WORKDIR=$TOPDIR/DistanceVL53L0X

PORT=12347

. $BINDIR/activate
echo "VIRTUAL_ENV=$VIRTUAL_ENV"

cd $WORKDIR
while true; do
    if [ $# -gt 0 ]; then
        echo ----- pip install
        pip install .
    fi

    echo "----- START distancevl53l0x server"
    python3 -m distancevl53l0x server -p $PORT
    echo "----- END   distancevl53l0x server"

    sleep 5
done
