#!/bin/sh

VENVDIR=$HOME/env2-robottank
BINDIR=$VENVDIR/bin
WORKDIR=$VENVDIR/mjpg-streamer/mjpg-streamer-experimental

PORT=8080

DELAY=2000

WIDTH=1920
HEIGHT=1080
FPS=20
ROT=180

. $BINDIR/activate

cd $WORKDIR
pwd
# exec ./mjpg_streamer -o "./output_http.so -w ./www -p $PORT" -i "./input_raspicam.so -x 1920 -y 1080 -fps $FPS -q 10 $ROT -vs"

while true; do
    waitbtn.py TR

    ./mjpg_streamer -o "./output_http.so -w ./www -p $PORT" -o "output_file.so -f $HOME/tmp/pics -d $DELAY" -i "./input_raspicam.so -x $WIDTH -y $HEIGHT -fps $FPS -q 10 -rot $ROT" &
    PID=$!

    waitbtn.py TL

    kill $PID

    sleep 1
done