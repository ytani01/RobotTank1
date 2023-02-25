#
# Copyright (c) 2023 Yoichi Tanibayashi
#
# -*- coding: utf-8 -*-
#
from cmdclientserver import CmdClient
from .dcmtr_server import DEF_PORT
from .my_logger import get_logger


class DcMtrClient:
    def __init__(self, svr_host='localhost', svr_port=DEF_PORT, debug=False):
        self._dbg = debug
        __class__.__log = get_logger(__class__.__name__, self._dbg)
        self.__log.debug('svr=%s:%s', svr_host, svr_port)

        self._svr_host = svr_host
        self._svr_port = svr_port

        self._clnt = CmdClient(self._svr_host, self._svr_port, self._dbg)

    def set_speed(self, speed):
        """
        Parameters
        ----------
        speed: list(int)
        """
        self.__log.debug('speed=%s', speed)

        ret = self._clnt.call('SPEED %s %s' % (int(speed[0]), int(speed[1])))
        self.__log.debug('ret=%s', ret)

    def set_stop(self):
        self.__log.debug('')

        ret = self._clnt.call('STOP')
        self.__log.debug('ret=%s', ret)

    def set_break(self):
        self.__log.debug('')

        ret = self._clnt.call('BREAK')
        self.__log.debug('ret=%s', ret)

    def set_delay(self, delay: float):
        """
        Parameters
        ----------
        delay: float
        """
        self.__log.debug('delay=%s', delay)

        ret = self._clnt.call('DELAY %s' % (delay))
        self.__log.debug('ret=%s', ret)

    def set_clear(self):
        self.__log.debug('')

        ret = self._clnt.call('CLEAR')
        self.__log.debug('ret=%s', ret)
