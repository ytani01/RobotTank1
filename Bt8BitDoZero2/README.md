# Bt8BitDoZero2 - 8BitDo zero 2

Bluetooth gamepad

## Setup

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
$ ls /dev/input/js0
(check a number of device file)

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
event at 1676375760.738340, code 04, type 04, val 589828
event at 1676375760.738340, code 307, type 01, val 01
event at 1676375760.738340, code 00, type 00, val 00
event at 1676375760.858367, code 04, type 04, val 589828
event at 1676375760.858367, code 307, type 01, val 00
event at 1676375760.858367, code 00, type 00, val 00
:
[Ctrl]-C
```


## Software Architecture

``` text
```
