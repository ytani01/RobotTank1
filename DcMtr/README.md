# DC Motor

DC Motor package

## Install

``` shell
cd ~
python3 -m venv env1
cd ~/env1
. ./bin/activate

git clone git@github.com:ytani01/RobotTank1.git

cd ~/env1/RobotTank1
git clone git@github.com:ytani01/CuiLib.git
cd ~/env1/RobotTank1/CuiLib
pip install .

cd ~/env1/RobotTank1/CmdClientServer
pip install .

cd ~/env1/RobotTank1/DcMtr
pip install pigpio click
pip install .
```

## samples

### server
``` shell
python3 -m dcmtr server 17 18 13 12
```

### client

``` shell
./sample_dcmtr_client.py
```


## Software Architecture

``` text
+-------------+
| DcMtrClient |
+-------------+
|  CmdClient  |
+-------------+
       |
       | TCP/IP
       v
+--------- server
|  CmdServer    |
|---------------|
|  |   DcMtrN   |
|  |------------|
|  |   DcMtr    |
|  +------------|
+---------------+
```
