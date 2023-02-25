#!/usr/bin/env python3
#
# Copyright (c) 2023 Yoichi Tanibayashi
#
# -*- coding: utf-8 -*-
#
import sys
import click
import cuilib
from dcmtr import DcMtrClient, get_logger


class App:
    """ Test DcMtrN class """

    DEF_STD_SPEED = [60, 60]
    D_V = 20
    ADJ_V = 5
    ROT_RATIO = 0.7
    CURV_RATIO = 0.4

    def __init__(self, svrhost, svrport, debug):
        self.dbg = debug
        __class__.__log = get_logger(__class__.__name__, debug)
        self.__log.debug('svr=%s:%s', svrhost, svrport)

        self._svrhost = svrhost
        self._svrport = svrport

        self._mtr = DcMtrClient(self._svrhost, self._svrport, self.dbg)
        self.cui = cuilib.Cui()

        self.std_speed = self.DEF_STD_SPEED
        self.__log.debug('std_speed=%s', self.std_speed)
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
        self.__log.info('speed=%s', self.speed)
        self._mtr.set_speed(self.speed)

    def forward(self, key_sym):
        self.speed = [s for s in self.std_speed]  # 値渡し！
        self.set_speed()

    def backward(self, key_sym):
        self.speed = [-s for s in self.std_speed]
        self.set_speed()

    def l_up(self, key_sym):
        self.std_speed[0] += self.ADJ_V
        self.__log.debug('std_speed=%s', self.std_speed)
        self.forward(key_sym)

    def r_up(self, key_sym):
        self.std_speed[1] += self.ADJ_V
        self.__log.debug('std_speed=%s', self.std_speed)
        self.forward(key_sym)

    def l_down(self, key_sym):
        self.std_speed[0] -= self.ADJ_V
        self.__log.debug('std_speed=%s', self.std_speed)
        self.forward(key_sym)

    def r_down(self, key_sym):
        self.std_speed[1] -= self.ADJ_V
        self.__log.debug('std_speed=%s', self.std_speed)
        self.forward(key_sym)

    def l_rot(self, key_sym):
        if self.speed == [0, 0]:
            self.speed[0] = -self.std_speed[0] * self.ROT_RATIO
            self.speed[1] = self.std_speed[1] * self.ROT_RATIO
        else:
            self.speed[0] = self.std_speed[0] * self.CURV_RATIO
            self.speed[1] = self.std_speed[1]

        self.set_speed()

    def r_rot(self, key_sym):
        if self.speed == [0, 0]:
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
        self._mtr.set_break()
        self.set_stop(key_sym)

    def quit(self, key_sym):
        self.__log.info('')
        self.set_stop(key_sym)
        self.cui.end()


@click.command(context_settings=dict(help_option_names=['-h', '--help']),
               help="Test DcMtrN Package")
@click.option('--svrhost', '-s', 'svrhost', type=str, default='localhost',
              help='server host')
@click.option('--svrport', '-p', 'svrport', type=int, default=12345,
              help='server host')
@click.option('--debug', '-d', 'debug', is_flag=True, default=False,
              help='debug flag')
def main(svrhost, svrport, debug):
    __log = get_logger(__name__, debug)
    __log.debug('svr=%s:%s', svrhost, svrport)

    res = 0
    app = App(svrhost, svrport, debug)

    try:
        print('START')
        app.main()

    finally:
        print('END')
        sys.exit(res)


if __name__ == '__main__':
    main()
