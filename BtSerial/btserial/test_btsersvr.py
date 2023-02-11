#!/usr/bin/env python3
#
# Copyright (c) 2023 Yoichi Tanibayashi
#
# -*- coding: utf-8 -*-
#
import click
import time
from .my_logger import get_logger
from . import BtSerSvr


class Test_BtSerSvr:
    """ Test BtSerSvr class """

    def __init__(self, debug=False):
        self._dbg = debug
        __class__.__log = get_logger(__class__.__name__, self._dbg)
        self.__log.debug('')

    def main(self):
        self.__log.debug('')

        btsersvr = BtSerSvr(BtSerSvr.DEF_PORT, self.cb_func, debug=self._dbg)
        btsersvr.start()

        while True:
            self.__log.debug('running')
            time.sleep(5)

    def cb_func(self, data):
        """ callback function """
        self.__log.info('data=%a', data)


@click.command(help="Bluetooth Serial Server Test")
@click.option('--debug', '-d', 'debug', is_flag=True, default=False,
              help='debug flag')
@click.pass_obj
def btsersvr(obj, debug):
    """ kbd """
    __log = get_logger(__name__, obj['debug'] or debug)
    __log.debug('obj=%s', obj)

    test_app = Test_BtSerSvr(obj['debug'] or debug)

    try:
        test_app.main()

    finally:
        print('END')
