#!/usr/bin/env python3
#
# Copyright (c) 2023 Yoichi Tanibayashi
#
# -*- coding: utf-8 -*-
#
import time
from .my_logger import get_logger
from . import DcMtr


class DcMtrN:
    """ DcMtrN """

    def __init__(self, pi, pin, debug=False):
        """ constructor """
        self._dbg = debug
        __class__.__log = get_logger(__class__.__name__, self._dbg)
        self.__log.debug('pin=%s', pin)

        self._pi = pi
        self._pin = pin

        self._mtr_n = len(self._pin)
        self._dc_mtr = list(range(self._mtr_n))

        for i in range(self._mtr_n):
            self._dc_mtr[i] = DcMtr(self._pi, self._pin[i], debug)

    def set_speed(self, speed):
        # 逆起電力対策
        self.set_stop()
        time.sleep(0.03)  # XXX 要調整

        ret_speed = []
        for i in range(self._mtr_n):
            ret_speed.append(self._dc_mtr[i].set_speed(speed[i]))

        self.__log.debug("ret_speed=%s", ret_speed)
        return ret_speed

    def set_break(self):
        for i in range(self._mtr_n):
            self._dc_mtr[i].set_break()

    def set_stop(self):
        for i in range(self._mtr_n):
            self._dc_mtr[i].set_stop()
