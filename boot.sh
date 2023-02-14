#!/bin/sh

VENVDIR=$HOME/env2-robottank
BINDIR=$VENVDIR/bin
ROBOTDIR=$VENVDIR/RobotTank1

$ROBOTDIR/start_server.sh &

sleep 2

#exec $ROBOTDIR/start_kbd.sh
exec $ROBOTDIR/start_bt8bitdozero2.sh
