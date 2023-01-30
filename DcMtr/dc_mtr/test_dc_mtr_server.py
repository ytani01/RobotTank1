#!/usr/bin/env python3
#
# Copyright (c) 2023 Yoichi Tanibayashi
#
# -*- coding: utf-8 -*-
#
from .my_logger import get_logger
from . import DcMtrServer


class Test_DcMtrServer:
    def __init__(self, pi, pin, port, debug=False):
        self._dbg = debug
        __class__.__log = get_logger(__class__.__name__, self._dbg)
        self._pi = pi
        self._pin = pin
        self._port = port
        self.__log.debug('pin=%s, port=%s', self._pin, self._port)

        self._svr = DcMtrServer(
            self._pi, self._pin, self._port, debug=self._dbg)

    def main(self):
        self.__log.info('start server')

        try:
            self._svr.serve_forever()
        except ValueError as e:
            self.__log.error('port=%s: is in use (?)', self._port)
            self.__log.error('  %s:%s', type(e).__name__, e)
        except Exception as e:
            self.__log.error('%s:%s', type(e).__name__, e)
        except KeyboardInterrupt as e:
            self.__log.info('%s:%s', type(e).__name__, e)
            pass

        self.__log.debug('done')
