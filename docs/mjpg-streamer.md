# mjpg-streamer

## Install

``` sh
cd $VIRTURAL_VENV
sudo apt install -y git cmake libjpeg-dev
git clone https://github.com/neuralassembly/mjpg-streamer.git
cd mjpg-streamer/mjpg-streamer-experimental
make
```

## camera test

``` sh
vcgencmd get_camera
:
raspistill -n -o pi-camera.jpg
:
```

## Usage

Web Server
``` sh
./mjpg_streamer -o "./output_http.so -w ./www -p 8080" -i "./input_raspicam.so -x 1920 -y 1080 -fps $FPS -q 10 -rot 180 -vs"
```

Save jpeg files
``` sh
mkdir $HOME/tmp/pics
./mjpg_streamer -o "./output_http.so -w ./www -p 8080" -o "output_file.so -f $HOME/tmp/pics -d 2000" -i "./input_raspicam.so -x 1920 -y 1080 -fps 30 -q 10 -rot 180"
```

## Reference

* [Raspberry PiでMJPG-Streamerを使って監視カメラを作ってみよう](https://ponkichi.blog/mjpg-streamer/)

* [「ラズパイのカメラ動画保存方法」MJPG-streamerから簡単に出来ます！](https://denkenmusic.com/%E3%80%8C%E3%83%A9%E3%82%BA%E3%83%91%E3%82%A4%E3%81%AE%E3%82%AB%E3%83%A1%E3%83%A9%E5%8B%95%E7%94%BB%E4%BF%9D%E5%AD%98%E6%96%B9%E6%B3%95%E3%80%8Dmjpg-streamer%E3%81%8B%E3%82%89%E7%B0%A1%E5%8D%98/)
