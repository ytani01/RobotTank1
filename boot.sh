#!/bin/sh

#sudo swapoff -a

VENVDIR=$HOME/env2-robottank
BINDIR=$VENVDIR/bin
ROBOTDIR=$VENVDIR/RobotTank1

. $BINDIR/activate
echo "$0: VIRTUAL_ENV=$VIRTUAL_ENV"

while true; do
#    $ROBOTDIR/start_mjpg-streamer.sh &

    $ROBOTDIR/start_dc_server.sh &
    $ROBOTDIR/start_distance_server.sh &

    sleep 2

    $ROBOTDIR/start_bt8bitdozero2.sh &

    $ROBOTDIR/start_auto.sh &

    while true; do
	$BINDIR/waitbtn.py ST
	if [ $? -eq 0 ]; then
	    break
	fi
    done

    pkill start
    pkill python3
    pkill mjpg

    sleep 5
done
