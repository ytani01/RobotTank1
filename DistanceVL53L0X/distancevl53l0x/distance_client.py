#
# Copyright (c) 2023 Yoichi Tanibayahshi
#
# -*- coding: utf-8 -*-
#
from cmdclientserver import CmdClient, get_logger
from . import DEF_PORT


class DistanceClient:
    def __init__(self, svr_host='localhost', svr_port=DEF_PORT, debug=False):
        self._dbg = debug
        __class__.__log = get_logger(__class__.__name__, self._dbg)
        self.__log.debug('svr=%s:%s', svr_host, svr_port)

        self._svr_host = svr_host
        self._svr_port = svr_port

        self._clnt = CmdClient(self._svr_host, self._svr_port, self._dbg)

    def get_distance(self):
        """
        Returns
        -------
        distance: float .. < 0: ERROR
        """
        rep = self._clnt.call('GET_DISTANCE').split()
        self.__log.debug('rep=%s', rep)

        if rep[0] == 'NG':
            self.__log.error('%s', rep)
            return -1.0

        try:
            distance = float(rep[1])
            return float(distance)
        except Exception as e:
            self.__log.error('%s:%s', type(e).__name__, e)
            return -2.0
