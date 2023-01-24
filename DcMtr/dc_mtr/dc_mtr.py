#!/usr/bin/env python3
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
        self.dbg = debug
        self.__log = get_logger(__class__.__name__, self.dbg)
        self.pi = pi
        self.pin = pin
        self.__log.debug('pin=%s', pin)

        self.n = len(pin)
        self.pwm_freq = list(range(self.n))
        self.pwm_range = list(range(self.n))
        self.__log.debug('n=%s, pwm_freq=%s, pwm_range=%s',
                         self.n, self.pwm_freq, self.pwm_range)

        for i in range(self.n):
            pi.set_mode(pin[i], pigpio.OUTPUT)
            self.pwm_freq[i] = pi.set_PWM_frequency(pin[i], DcMtr.PWM_FREQ)
            self.pwm_range[i] = pi.set_PWM_range(pin[i], DcMtr.PWM_RANGE)
            pi.set_PWM_dutycycle(pin[i], 0)

    def set(self, in1, in2):
        if in1 < 0:
            in1 = 0
        if in1 > DcMtr.PWM_RANGE:
            in1 = DcMtr.PWM_RANGE
        if in2 < 0:
            in2 = 0
        if in2 > DcMtr.PWM_RANGE:
            in2 = DcMtr.PWM_RANGE

        self.pi.set_PWM_dutycycle(self.pin[0], in1)
        self.pi.set_PWM_dutycycle(self.pin[1], in2)

    def set_speed(self, speed, sec=0):
        if speed < -DcMtr.PWM_RANGE:
            speed = -DcMtr.PWM_RANGE
        if speed > DcMtr.PWM_RANGE:
            speed = DcMtr.PWM_RANGE

        if speed >= 0:
            self.set(speed, 0)
        else:
            self.set(0, -speed)

        time.sleep(sec)

    def set_break(self, sec=0):
        self.set(DcMtr.PWM_RANGE,DcMtr.PWM_RANGE)
        time.sleep(sec)

    def set_stop(self, sec=0):
        self.set(0,0)
        time.sleep(sec)


class DcMtrN:
    """ DcMtrN """
    def __init__(self, pi, pin, debug=False):
        self.dbg = debug
        self.__log = get_logger(__class__.__name__, self.dbg)
        self.pi = pi
        self.n = len(pin)
        self.dc_mtr = list(range(self.n))

        for i in range(self.n):
            self.dc_mtr[i] = DcMtr(self.pi, pin[i], debug)

    def set_speed(self, speed, sec=0):
        for i in range(self.n):
            self.dc_mtr[i].set_speed(speed[i])
        time.sleep(sec)

    def set_break(self, sec=0):
        for i in range(self.n):
            self.dc_mtr[i].set_break()
        time.sleep(sec)

    def set_stop(self, sec=0):
        for i in range(self.n):
            self.dc_mtr[i].set_stop()
        time.sleep(sec)
