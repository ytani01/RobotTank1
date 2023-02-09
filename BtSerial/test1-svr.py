#!/usr/bin/env python3

import bluetooth

while True:
    svr_sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)

    print("connecting ... ")

    svr_sock.bind(("", 1))
    svr_sock.listen(1)

    client_sock, addr = svr_sock.accept()

    print("connected")

    while True:
        try:
            data = client_sock.recv(1024)
            # data = data.decode()
            print(data)
            print('\n')

        except Exception as e:
            print("%s:%s" % (type(e).__name__, e))
            client_sock.close()
            svr_sock.close()
            break
