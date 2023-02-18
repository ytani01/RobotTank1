#!/usr/bin/env python3
#
# Copyright (c) 2023 Yoichi Tanibayahshi
#
# -*- coding: utf-8 -*-
#
import telnetlib
import time
import json
from .my_logger import get_logger


class DcMtrClient:
    """ DcMtrClient
    """
    DEF_HOST = 'localhost'
    DEF_PORT = 12345

    def __init__(self, svr_host=DEF_HOST, svr_port=DEF_PORT, debug=False):
        """ init """
        self._dbg = debug
        __class__.__log = get_logger(__class__.__name__, self._dbg)
        self.__log.debug('svr: %s:%s', svr_host, svr_port)

        self._svr_host = svr_host
        self._svr_port = svr_port

        self._tn = None

    def __del__(self):
        self.__log.debug('')

    def recv_reply(self):
        self.__log('')

        buf = b''

        while True:
            time.sleep(0.1)
            try:
                in_data = self._tn.read_eager()
            except Exception as e:
                self.__log.warning('%s:%s', type(e).__name__, e)
                in_data = b''

            if len(in_data) == 0:
                break

            self.__log.debug('in_data=%a', in_data)
            buf += in_data

        self.__log.debug('buf=%a', buf)

        try:
            ret_str = buf.decode('utf-8')
        except UnicodeDecodeError:
            if buf == b'':
                ret_str = ''
            else:
                ret_str = str(buf)

        self.__log.debug('ret_str=%a', ret_str)

        try:
            ret = json.loads(ret_str)
        except json.decoder.JSONDecodeError:
            ret = {'CMD': '', 'ACCEPT': '', 'MSG': ret_str}

        self.__log.debug('ret=%s', ret)

        return ret

    def send_cmdline(self, cmdline):
        self.__log.debug('cmdline=%s', cmdline)

        try:
            self._tn = telnetlib.Telnet(self._svr_host, self._svr_port)
            self._tn.write(cmdline.encode('utf-8'))
            time.sleep(0.01)
            self._tn.close()
        except Exception as e:
            self.__log.error('%s:%s', type(e).__name__, e)

        return cmdline
