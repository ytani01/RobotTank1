#!/usr/bin/env python3
#
# -*- coding: utf-8 -*-
#
import cuilib
from .my_logger import get_logger
from . import DcMtrN


class Test_DcMtrN:
    """ Test DcMtrN class """

    DEF_STD_SPEED = [60, 60]
    D_V = 20
    ADJ_V = 5
    ROT_RATIO = 0.7
    CURV_RATIO = 0.4

    def __init__(self, pi, pin, debug):
        self.dbg = debug
        self.__log = get_logger(__class__.__name__, debug)
        self.pi = pi
        self.pin = pin
        self.__log.debug('pin=%s', pin)

        self.dc_mtr_n = DcMtrN(self.pi, pin, self.dbg)
        self.cui = cuilib.Cui()

        self.std_speed = __class__.DEF_STD_SPEED
        self.speed = [0, 0]

    def main(self):
        self.cui.add('hH?', self.cui.help, 'command help')
        self.cui.add(['Q', 'KEY_ESCAPE'], self.quit, 'quit')

        self.cui.add('w', self.forward, 'Forward')
        self.cui.add('x', self.backward, 'Backward')

        self.cui.add('q', self.l_up, 'Left Up')
        self.cui.add('e', self.r_up, 'Right Up')

        self.cui.add('z', self.l_down, 'Left Down')
        self.cui.add('c', self.r_down, 'Right Down')
        
        self.cui.add('a', self.l_rot, 'Rotate Left')
        self.cui.add('d', self.r_rot, 'Rotate Right')

        self.cui.add('s', self.set_stop, 'Stop')
        self.cui.add('b', self.set_break, 'Break')

        self.cui.start()
        self.cui.join()

    def set_speed(self):
        self.speed = self.dc_mtr_n.set_speed(self.speed)
        self.__log.info('speed=%s', self.speed)

    def forward(self, key_sym):
        self.speed = self.std_speed
        self.set_speed()

    def backward(self, key_sym):
        self.speed = [-s for s in self.std_speed]
        self.set_speed()

    def l_up(self, key_sym):
        self.std_speed[0] += self.ADJ_V
        self.forward(key_sym)

    def r_up(self, key_sym):
        self.std_speed[1] += self.ADJ_V
        self.forward(key_sym)

    def l_down(self, key_sym):
        self.std_speed[0] -= self.ADJ_V
        self.forward(key_sym)

    def r_down(self, key_sym):
        self.std_speed[1] -= self.ADJ_V
        self.forward(key_sym)

    def l_rot(self, key_sym):
        if ( self.speed == [0, 0] ):
            self.speed[0] = -self.std_speed[0] * self.ROT_RATIO
            self.speed[1] = self.std_speed[1] * self.ROT_RATIO
        else:
            self.speed[0] = self.std_speed[0] * self.CURV_RATIO
            self.speed[1] = self.std_speed[1]

        self.set_speed()

    def r_rot(self, key_sym):
        if ( self.speed == [0, 0] ):
            self.speed[0] = self.std_speed[1] * self.ROT_RATIO
            self.speed[1] = -self.std_speed[1] * self.ROT_RATIO
        else:
            self.speed[0] = self.std_speed[1]
            self.speed[1] = self.std_speed[1] * self.CURV_RATIO

        self.set_speed()

    def set_stop(self, key_sym):
        self.speed = [0, 0]
        self.set_speed()

    def set_break(self, key_sym):
        self.__log.info('')
        self.dc_mtr_n.set_break()
        self.set_stop(key_sym)

    def quit(self, key_sym):
        self.__log.info('')
        self.set_break(key_sym)
        self.cui.end()
