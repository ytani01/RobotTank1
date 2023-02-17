#!/usr/bin/env python3
#
# Copyright (c) 2023 Yoichi Tanibayashi
#
# -*- coding: utf-8 -*-
#
import click
import time
import evdev
from .my_logger import get_logger
from . import Bt8BitDoZero2


class Test_Bt8BitDoZero2:
    """ Test Bt8BitDoZero2 class """

    def __init__(self, devs, debug=False):
        self._dbg = debug
        __class__.__log = get_logger(__class__.__name__, self._dbg)
        self.__log.debug('devs=%s', devs)

        self._devs = devs

        self._bt8bitdozero2 = Bt8BitDoZero2.get_bt8bitdozero2(
            self._devs, self.cb_func, self._dbg)
        self.__log.debug('bt8bitdozero2=%s', self._bt8bitdozero2)

    def main(self):
        self.__log.debug('')

        for b in self._bt8bitdozero2:
            b.start()

        while True:
            print(time.strftime('%Y/%m/%d(%a) %H:%M:%S'))
            time.sleep(5)

    def cb_func(self, dev, evtype, code, value):
        """ callback function """
        self.__log.info('dev=%d, evtype=%d:%s, code=%d:%s, value=%d:%s',
                        dev, evtype, evdev.ecodes.EV[evtype],
                        code, Bt8BitDoZero2.keycode2str(evtype, code),
                        value, Bt8BitDoZero2.keyval2str(evtype, value))


@click.command(help="Bluetooth Keyboard Test")
@click.argument('devs', metavar='dev_num[0|1|2|3..]...', type=int, nargs=-1)
@click.option('--debug', '-d', 'debug', is_flag=True, default=False,
              help='debug flag')
@click.pass_obj
def bt8bitdozero2(obj, devs, debug):
    """ bt8bitdozero2 """
    __log = get_logger(__name__, obj['debug'] or debug)
    __log.debug('obj=%s, devs=%s', obj, devs)

    test_app = Test_Bt8BitDoZero2(devs, obj['debug'] or debug)

    try:
        test_app.main()

    finally:
        print('END')
