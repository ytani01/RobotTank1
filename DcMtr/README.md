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
|-----------------|        | DcMtrWorker | |
|  | DcMtrHandler | -----> |  (thread)   | |
|   --------------   cmdq  |-------------| |
|                          |   DcMtrN    | |
|                          |-------------| |
|                          |   DcMtr     | |
|                           -------------  |
 ------------------------------------------
```
