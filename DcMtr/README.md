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
 ------------------------------------------
| DcMtrServer     |         -------------  |
|    DcMtrHandler | -----> | DcMtrWorker | |
|                 |  cmdq  |  (thread)   | |
|-----------------         |-------------| |
|                          |   DcMtrN    | |
|                          |-------------| |
|                          |   DcMtr     | |
|                           -------------  |
 ------------------------------------------
```
