#!/usr/bin/env python3
#
# Copyright (c) 2023 Yoichi Tanibayashi
#
# -*- coding: utf-8 -*-
#
import click
import time
import cuilib
from .my_logger import get_logger
from . import AbShutter


class Test_AbShutter:
    """ Test AbShutter class """

    def __init__(self, devs, debug=False):
        self._dbg = debug
        __class__.__log = get_logger(__class__.__name__, self._dbg)
        self.__log.debug('devs=%s', devs)

        self._devs = devs

        self._obj = []
        for d in self._devs:
            self._obj.append(AbShutter(d, self.cb_func, debug=self._dbg))

    def main(self):
        self.__log.debug('')
        
        for o in self._obj:
            o.start()

        while True:
            print(time.strftime('%Y/%m/%d(%a) %H:%M:%S'))
            time.sleep(5)

    def cb_func(self, dev, code, value):
        """ callback function """
        self.__log.debug('')
        
        print('dev=%d, code=%d:%s, value=%d:%s' %
              (dev,
               code, AbShutter.keycode2str(code),
               value, AbShutter.keyval2str(value)))


@click.command(help="ab_shutter")
@click.argument('devs', metavar='[0|1|2|4..]...', type=int, nargs=-1)
@click.option('--debug', '-d', 'debug', is_flag=True, default=False,
              help='debug flag')
@click.pass_obj
def ab_shutter(obj, devs, debug):
    """ ab_shutter """
    __log = get_logger(__name__, obj['debug'] or debug)
    __log.debug('obj=%s, devs=%s', obj, devs)

    test_app = Test_AbShutter(devs, obj['debug'] or debug)

    try:
        test_app.main()

    finally:
        print('END')
