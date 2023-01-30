#!/usr/bin/env python3
#
# Copyright (c) 2023 Yoichi Tanibayashi
#
# -*- coding: utf-8 -*-
#
import sys
from .my_logger import get_logger
from . import DcMtrClient


class Test_DcMtrClient:
    """ Test_DcMtrClient """

    def __init__(self, svr_host, svr_port, cmdline='', debug=False):
        self._dbg = debug
        __class__.__log = get_logger(__class__.__name__, self._dbg)
        self.__log.debug('svr: %s:%s', svr_host, svr_port)

        self._svr_host = svr_host
        self._svr_port = svr_port
        self._cmdline = cmdline

        self._clnt = DcMtrClient(self._svr_host, self._svr_port, debug=self._dbg)

    def main(self):
        self.__log.debug('')

        if len(self._cmdline) > 0:
            self._clnt.send_cmdline(self._cmdline)
            return

        while True:
            cmdline = sys.stdin.readline().strip()
            if len(self._clnt.send_cmdline(cmdline)) == 0:
                break
