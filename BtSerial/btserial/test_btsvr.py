#!/usr/bin/env python3
#
# Copyright (c) 2023 Yoichi Tanibayashi
#
# -*- coding: utf-8 -*-
#
import click
import time
from .my_logger import get_logger
from . import BtKbd


class Test_Kbd:
    """ Test Kbd class """

    def __init__(self, devs, debug=False):
        self._dbg = debug
        __class__.__log = get_logger(__class__.__name__, self._dbg)
        self.__log.debug('devs=%s', devs)

        self._devs = devs

        self._btkbd = []
        for d in self._devs:
            btkbd = None
            while btkbd is None:
                try:
                    btkbd = BtKbd(d, self.cb_func, debug=self._dbg)
                except Exception as e:
                    self.__log.error('%s:%s', type(e).__name__, e)
                    time.sleep(2)
                else:
                    self.__log.info('Connected: %s', d)

            self._btkbd.append(btkbd)

    def main(self):
        self.__log.debug('')
        
        for btkbd in self._btkbd:
            btkbd.start()

        while True:
            print(time.strftime('%Y/%m/%d(%a) %H:%M:%S'))
            time.sleep(5)

    def cb_func(self, dev, code, value):
        """ callback function """
        self.__log.info('dev=%d, code=%d:%s, value=%d:%s',
                        dev,
                        code, BtKbd.keycode2str(code),
                        value, BtKbd.keyval2str(value))


@click.command(help="Bluetooth Keyboard Test")
@click.argument('devs', metavar='dev_num[0|1|2|3..]...', type=int, nargs=-1)
@click.option('--debug', '-d', 'debug', is_flag=True, default=False,
              help='debug flag')
@click.pass_obj
def kbd(obj, devs, debug):
    """ kbd """
    __log = get_logger(__name__, obj['debug'] or debug)
    __log.debug('obj=%s, devs=%s', obj, devs)

    test_app = Test_Kbd(devs, obj['debug'] or debug)

    try:
        test_app.main()

    finally:
        print('END')
