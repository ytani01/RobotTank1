#!/usr/bin/env python3
#
# Copyright (c) 2023 Yoichi Tanibayashi
#
# -*- coding: utf-8 -*-
#
import bluetooth
import threading
from .my_logger import get_logger


class BtSerSvr(threading.Thread):
    DEF_PORT = 1
    NUM_LISTEN = 0
    BUFSIZE = 512

    def __init__(self, port=DEF_PORT, cb_func=None, debug=False):
        self._dbg = debug
        __class__.__log = get_logger(__class__.__name__, self._dbg)
        self.__log.debug('port=%d', port)

        self._port = port
        self._cb = cb_func
        
        super().__init__(daemon=True)

    def run(self):
        self.__log.debug('')

        while True:
            svr_sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)

            svr_sock.bind(("", self._port))
            svr_sock.listen(self.NUM_LISTEN)

            self.__log.info('waiting ...')

            clnt_sock, addr = svr_sock.accept()

            self.__log.info('connected:%s', addr)

            while True:
                try:
                    data = clnt_sock.recv(self.BUFSIZE)
                    data_str = data.decode('utf-8')
                    self.__log.debug('data=%a', data)

                    if self._cb is not None:
                        self._cb(data_str)

                except Exception as e:
                    self.__log.warning('%s:%s', type(e).__name__, e)
                    clnt_sock.close()
                    svr_sock.close()
                    break
