# BtSerial - Bluetooth Serial

Bluetooh Serial Server

## Setup

### Bluetooth pairing

#### 1. ペアリング待受け

``` shell
$ sudo bluetoothctl
[...]# 
```

#### 2. スマホからペアリング


#### 3. パスキーによる承認

``` shell
[...]#
Request confirmation
[agent] Confirm passkey 198156 (yes/no): yes
```

一旦コネクトした後に切れてよい


### bluetoothd 設定

/usr/lib/systemd/system/bluetooth.service
```
- ExecStart=/usr/libexec/bluetooth/bluetoothd
+ ExecStart=/usr/libexec/bluetooth/bluetoothd -C
+ ExecStartPost=/usr/bin/sdptool add SP
```
