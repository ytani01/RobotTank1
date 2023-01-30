#!/usr/bin/env python3
#
# Copyright (c) 2023 Yoichi Tanibayashi
#
# -*- coding: utf-8 -*-
#
import pigpio
import click
import cuilib
from .my_logger import get_logger
from . import DcMtr


class Test_DcMtr:
    """ Test DcMtr class """

    def __init__(self, pi, pin, debug):
        self._dbg = debug
        __class__.__log = get_logger(__class__.__name__, self._dbg)
        self.pi = pi
        self.pin = pin
        self.__log.debug('pin=%s', pin)

        self.dc_mtr = DcMtr(self.pi, pin, self._dbg)
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


@click.command(help="dc_mtr")
@click.argument('pin1', type=int)
@click.argument('pin2', type=int)
@click.option('--opt1', '-o1', 'opt1', type=str, default=None, help='opt')
@click.option('--debug', '-d', 'debug', is_flag=True, default=False,
              help='debug flag')
@click.pass_obj
def dc_mtr(obj, pin1, pin2, opt1, debug):
    """ dc_mtr """
    __log = get_logger(__name__, obj['debug'] or debug)
    __log.debug('obj=%s, opt1=%s, args=%s', obj, opt1, (pin1, pin2))

    pi = pigpio.pi()
    test_app = Test_DcMtr(pi, (pin1, pin2), obj['debug'] or debug)

    try:
        test_app.main()

    finally:
        pi.stop()
