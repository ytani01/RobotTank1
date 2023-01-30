# DC Motor

DC Motor package

## Software Architecture

``` text
 -------------
| DcMtrClient |
 -------------
       |
       | TCP/IP
       v
 ------------------------------------------------
| DcMtrServer     |               -------------  |
|    DcMtrHandler | --> cmdq --> | DcMtrWorker | |
|                 |              |  (thread)   | |
|-----------------               |-------------| |
|                                |   DcMtrN    | |
|                                |-------------| |
|                                |   DcMtr     | |
|                                 -------------  |
 ------------------------------------------------
```
