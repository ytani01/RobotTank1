#!/bin/sh

sudo swapoff -a

VENVDIR=$HOME/env2-robottank
BINDIR=$VENVDIR/bin
ROBOTDIR=$VENVDIR/RobotTank1

$ROBOTDIR/start_dc_server.sh &
$ROBOTDIR/start_distance_server.sh &

$ROBOTDIR/start_mjpg-streamer.sh &

sleep 2

#exec $ROBOTDIR/start_kbd.sh
$ROBOTDIR/start_bt8bitdozero2.sh &

$ROBOTDIR/start_auto.sh &
