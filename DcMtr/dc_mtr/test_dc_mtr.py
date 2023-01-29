#!/usr/bin/env python3
#
# -*- coding: utf-8 -*-
#
import cuilib
from .my_logger import get_logger
from . import DcMtr


class Test_DcMtr:
    """ Test DcMtr class """

    def __init__(self, pi, pin, debug):
        self.dbg = debug
        self.__log = get_logger(__class__.__name__, debug)
        self.pi = pi
        self.pin = pin
        self.__log.debug('pin=%s', pin)

        self.dc_mtr = DcMtr(self.pi, pin, self.dbg)
        self.cui = cuilib.Cui()

        self.speed = 0

    def main(self):
        self.cui.add('hH?', self.cui.help, 'command help')
        self.cui.add(['q', 'Q', 'KEY_ESCAPE'], self.quit, 'quit')

        self.cui.add('w', self.up, 'Up')
        self.cui.add('x', self.down, 'Down')
        self.cui.add('s', self.set_stop, 'Stop')
        self.cui.add('b', self.set_break, 'Break')

        self.cui.start()
        self.cui.join()

    def up(self, key_sym):
        self.speed += 5
        self.__log.info('spped=%s', self.speed)
        self.dc_mtr.set_speed(self.speed)

    def down(self, key_sym):
        self.speed -= 5
        self.__log.info('spped=%s', self.speed)
        self.dc_mtr.set_speed(self.speed)

    def set_stop(self, key_sym):
        self.speed = 0
        self.__log.info('spped=%s', self.speed)
        self.dc_mtr.set_speed(self.speed)

    def set_break(self, key_sym):
        self.__log.info('')
        self.dc_mtr.set_break()
        self.set_stop(key_sym)

    def quit(self, key_sym):
        self.__log.info('')
        self.set_break(key_sym)
        self.cui.end()
