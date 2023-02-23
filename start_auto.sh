#!/bin/sh

VENVDIR=$HOME/env2-robottank
BINDIR=$VENVDIR/bin
TOPDIR=$VENVDIR/RobotTank1
WORKDIR=$TOPDIR/DistanceVL53L0X

MTR_HOST=localhost
MTR_PORT=12345

D_HOST=localhost
D_PORT=12347

#DEVS="0 1"
DEVS="0"


. $BINDIR/activate
echo "VIRTUAL_ENV=$VIRTUAL_ENV"

cd $WORKDIR
pwd
while true; do
    if [ $# -gt 0 ]; then
        echo ----- pip install
        pip install .
    fi
    
    echo ----- distancevl53l0x robottankauto
    python3 -m distancevl53l0x robottankauto \
            --dc_host $MTR_HOST --dc_port=$MTR_PORT \
            --ds_host $D_HOST --ds_port=$D_PORT \
            $DEVS

    echo -----

    sleep 2
done
