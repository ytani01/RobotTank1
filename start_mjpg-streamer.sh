#!/bin/sh

VENVDIR=$HOME/env1-robot
BINDIR=$VENVDIR/bin
WORKDIR=$VENVDIR/mjpg-streamer/mjpg-streamer-experimental

PORT=8080

DELAY=2000

WIDTH=1920
HEIGHT=1080
#WIDTH=1280
#HEIGHT=720

FPS=30
#FPS=60

ROT=180

#VS=
VS=-vs

. $BINDIR/activate

cd $WORKDIR
pwd

while true; do
    waitbtn.py TR

    echo ----- mjpg_streamer
    ./mjpg_streamer -o "./output_http.so -w ./www -p $PORT" -o "output_file.so -f $HOME/tmp/pics -d $DELAY" -i "./input_raspicam.so -x $WIDTH -y $HEIGHT -fps $FPS -q 10 -rot $ROT $VS" &
    PID=$!

    waitbtn.py TL

    kill $PID

    sleep 1
done
