#!/bin/sh

VENVDIR=$HOME/env2-robottank
BINDIR=$VENVDIR/bin
TOPDIR=$VENVDIR/RobotTank1
WORKDIR=$TOPDIR

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
    echo ----- robottank_auto.py
    ./robottank_auto.py \
        --dc_host $MTR_HOST --dc_port=$MTR_PORT \
        --ds_host $D_HOST --ds_port=$D_PORT \
        $DEVS

    echo -----

    sleep 2
done
