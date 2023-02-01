#!/bin/sh

VENVDIR=$HOME/env2-robottank
BINDIR=$VENVDIR/bin
ROBOTDIR=$VENVDIR/RobotTank1

$ROBOTDIR/start_server.sh &

sleep 2

$ROBOTDIR/start_ab.sh
