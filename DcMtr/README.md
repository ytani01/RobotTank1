# DC Motor

DC Motor package

## Install



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
