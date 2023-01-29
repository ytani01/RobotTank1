#!/usr/bin/env python3
#
# Copyright (c) 2023 Yoichi Tanibayashi
#
# -*- coding: utf-8 -*-
#
import pigpio
import time
from .my_logger import get_logger


class DcMtr:
    """ DcMtr """

    PWM_FREQ = 50
    PWM_RANGE = 100

    def __init__(self, pi, pin, debug=False):
        self._dbg = debug
        __class__.__log = get_logger(__class__.__name__, self._dbg)
        self._pi = pi
        self._pin = pin
        self.__log.debug('pin=%s', self._pin)

        self._pin_n = len(pin)
        if self._pin_n != 2:
            self.__log.error('pin_n=%s', self._pin_n)
            
        self.speed = 0

        self._pwm_freq = list(range(self._pin_n))
        self._pwm_range = list(range(self._pin_n))

        for i in range(self._pin_n):
            self._pi.set_mode(pin[i], pigpio.OUTPUT)

            self._pwm_freq[i] = self._pi.set_PWM_frequency(self._pin[i],
                                                           DcMtr.PWM_FREQ)
            self._pwm_range[i] = self._pi.set_PWM_range(self._pin[i],
                                                        DcMtr.PWM_RANGE)
            self._pi.set_PWM_dutycycle(self._pin[i], 0)

        self.__log.debug('pwm_freq=%s, pwm_range=%s',
                         self._pwm_freq, self._pwm_range)

    def __set(self, in1, in2):
        in1 = max(in1, 0)
        in1 = min(in1, DcMtr.PWM_RANGE)

        in2 = max(in2, 0)
        in2 = min(in2, DcMtr.PWM_RANGE)

        self._pi.set_PWM_dutycycle(self._pin[0], in1)
        self._pi.set_PWM_dutycycle(self._pin[1], in2)

    def set_speed(self, speed):
        """
        -DcMtr.PWM_RANGE <= speed <= DcMtr.PWM_RANGE
        """
        self.speed = max(speed, -DcMtr.PWM_RANGE)
        self.speed = min(speed,  DcMtr.PWM_RANGE)

        self.__log.debug('speed=%s', self.speed)

        if self.speed >= 0:
            self.__set(self.speed, 0)
        else:
            self.__set(0, -self.speed)

        return self.speed

    def set_break(self):
        self.__set(DcMtr.PWM_RANGE, DcMtr.PWM_RANGE)
        self.speed = 0

    def set_stop(self):
        self.__set(0, 0)
        self.speed = 0
