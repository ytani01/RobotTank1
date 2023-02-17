#!/usr/bin/env python3
#
# Copyright (c) 2023 Yoichi Tanibayahshi
#
# -*- coding: utf-8 -*-
#
import telnetlib
import time
from .my_logger import get_logger


class Vl53l0xClient:
    """ Vl53l0xClient
    """
    DEF_HOST = 'localhost'
    DEF_PORT = 12346

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
        self.__log.debug('')

        # receive and decode
        try:
            # in_data = self._tn.read_eager()
            ret_str = self._tn.read_all().decode('utf-8')
        except UnicodeDecodeError as e:
            msg = '%s:%s' % (type(e).__name, e)
            self.__log.warning(msg)
            ret_str = msg
        except Exception as e:
            msg = '%s:%s' % (type(e).__name, e)
            self.__log.warning(msg)
            ret_str = msg

        self.__log.debug('ret_str=%a', ret_str)

        return ret_str

    def send_cmdline(self, cmdline):
        """
        send cmdline and receive reply
        """
        self.__log.debug('cmdline=%s', cmdline)

        self._tn = telnetlib.Telnet(self._svr_host, self._svr_port)

        self._tn.write(cmdline.encode('utf-8'))

        time.sleep(0.01)

        ret_str = self.recv_reply()
        return ret_str
