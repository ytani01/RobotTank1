# Bt8BitDoZero2 - 8BitDo zero 2

Bluetooth gamepad

## Setup

### Install

``` shell
pip install -U evdev click
pip install .
```


### 8BitDo zero 2

Power on: [B]+[start]


### Bluetooth pairing

``` shell
$ sudo bluetoothctl
[...]# power on
[...]# scan on
[...]# connect FF:FF:C1:21:B3:FB
[...]# pair FF:FF:C1:21:B3:FB
[...]# trust FF:FF:C1:21:B3:FB
[...]# quit
```


### Test

``` shell
$ ls /dev/input
(check a number of device file)

$ sudo apt install evtest
$ sudo evtest
:
... (BTN_NORTH) ...
... (BTN_SOUTH) ...
[Ctrl]-C

$ ./evdev-test1.py
devs: ['/dev/input/event0']
input_dev device /dev/input/event0, name "AB Shutter3       ", phys "B8:27:EB:73:30:CC"
---
Push buttons.. ([Ctrl]-C to end)
event at 1676375759.365823, code 04, type 04, val 589828
event at 1676375759.365823, code 307, type 01, val 01
event at 1676375759.365823, code 00, type 00, val 00
event at 1676375759.542115, code 04, type 04, val 589828
event at 1676375759.542115, code 307, type 01, val 00
event at 1676375759.542115, code 00, type 00, val 00
event at 1676375760.197109, code 04, type 04, val 589828
event at 1676375760.197109, code 307, type 01, val 01
event at 1676375760.197109, code 00, type 00, val 00
event at 1676375760.375814, code 04, type 04, val 589828
event at 1676375760.375814, code 307, type 01, val 00
event at 1676375760.375814, code 00, type 00, val 00
:
[Ctrl]-C
```


###

/etc/systemd/system/bluetooth.service.d/override.conf
``` text
:
ExecStart=/usr/libexec/bluetooth/bluetoothd --compat --noplugin=sap
ExecStartPost=/usr/bin/sdptool add SP
:
```

``` shell
sudo systemctl daemon-reload
sudo systemctl restart bluetooth.service
```

##

``` shell
python3 -m bt8bitdozero2 robottank 0
```

## Software Architecture

``` text
```
