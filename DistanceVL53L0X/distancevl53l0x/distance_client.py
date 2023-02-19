#
# Copyright (c) 2023 Yoichi Tanibayahshi
#
# -*- coding: utf-8 -*-
#
from cmdclientserver import CmdClient, get_logger


class DistanceClient:
    def __init__(self, svr_host, svr_port, debug=False):
        self._dbg = debug
        __class__.__log = get_logger(__class__.__name__, self._dbg)
        self.__log('svr=%s:%s', svr_host, svr_port)
