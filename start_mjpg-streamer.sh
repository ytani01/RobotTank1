#!/bin/sh

VENVDIR=$HOME/env2-robottank
WORKDIR=$VENVDIR/mjpg-streamer/mjpg-streamer-experimental

PORT=8080

DELAY=2000

WIDTH=1920
HEIGHT=1080
FPS=20
ROT="-rot 180"

cd $WORKDIR
pwd
# exec ./mjpg_streamer -o "./output_http.so -w ./www -p $PORT" -i "./input_raspicam.so -x 1920 -y 1080 -fps $FPS -q 10 $ROT -vs"
#exec ./mjpg_streamer -o "./output_http.so -w ./www -p $PORT" -o "output_file.so -f $HOME/tmp/pics -d $DELAY" -i "./input_raspicam.so -x $WIDTH -y $HEIGHT -fps $FPS -q 10 $ROT"
