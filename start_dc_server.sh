#!/bin/sh

VENVDIR=$HOME/env2-robottank
BINDIR=$VENVDIR/bin
TOPDIR=$VENVDIR/RobotTank1
WORKDIR=$TOPDIR/DcMtr

PINS="17 18 13 12"
PORT=12345

. $BINDIR/activate
echo "VIRTUAL_ENV=$VIRTUAL_ENV"

cd $WORKDIR
while true; do
    if [ $# -gt 0 ]; then
        echo ----- pip install
        pip install .
    fi

    echo "----- START dcmtr server"
    python3 -m dcmtr server -p $PORT $PINS
    echo "----- END   dcmtr server"

    sleep 5
done
