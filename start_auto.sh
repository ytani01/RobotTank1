#!/bin/sh

VENVDIR=$HOME/env1-robot
BINDIR=$VENVDIR/bin
TOPDIR=$VENVDIR/RobotTank1
WORKDIR=$TOPDIR
PKGDIR1=$TOPDIR/Bt8BitDoZero2
PKGDIR2=$TOPDIR/DistanceVL53L0X
PKGDIR3=$TOPDIR/DcMtr

MTR_HOST=localhost
MTR_PORT=12345

D_HOST=localhost
D_PORT=12347

#DEVS="0 1"
DEVS="0"


pipinstall() {
    echo ----- pip install $1
    _CWD=`pwd`
    
    cd $1
    pip install .

    cd $_CWD
}

. $BINDIR/activate
echo "VIRTUAL_ENV=$VIRTUAL_ENV"

cd $WORKDIR
pwd
while true; do
    if [ $# -gt 0 ]; then
        pipinstall $PKGDIR1
        pipinstall $PKGDIR2
        pipinstall $PKGDIR3
    fi

    echo ----- robottank_auto.py
    ./robottank_auto.py \
        --dc_host $MTR_HOST --dc_port=$MTR_PORT \
        --ds_host $D_HOST --ds_port=$D_PORT \
        $DEVS

    echo -----

    sleep 2
done
