# VL53L0X

VL53L0X: TOF Distance Sensor

## Install

###

``` shell
sudo apt install i2c-tools
```

### Gadgetoid/VL53L0X-python.git

``` shell
THISDIR=`pwd`
TOPDIR='../../'

pushd $TOPDIR

git clone git@github.com:Gadgetoid/VL53L0X-python.git

cd VL53L0X-python
make

cp ./bin/vl53l0x*.so $VIRTUAL_ENV/bin
cp ./python/VL53L0X.py $THISDIR/distancevl53l0x
cp ./python/VL53L0X_example.py $THISDIR/distancevl53l0x

popd

cd distancevl53l0x
patch -b < VL53L0X.py-patch
patch -b < VL53L0X_example.py-patch
```

### Python Package

``` shell
pip install -U smbus2 click
pip install .
```

### sample

``` shell
python3 -m distancevl53l0x distance
```

## server

``` shell
python3 -m distancevl53l0x server
```

## Software Architecture

``` text
```


## References

- [Gadgetoid/VL53L0X-python](https://github.com/Gadgetoid/VL53L0X-python)
