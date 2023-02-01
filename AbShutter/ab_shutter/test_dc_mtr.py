#!/usr/bin/env python3
#
# Copyright (c) 2023 Yoichi Tanibayashi
#
# -*- coding: utf-8 -*-
#
import click
import time
from dc_mtr import DcMtrClient
from .my_logger import get_logger
from . import AbShutter


class Test_DcMtr:
    """ Test AbShutter class """

    def __init__(self, devs, dc_mtr, debug=False):
        self._dbg = debug
        __class__.__log = get_logger(__class__.__name__, self._dbg)
        self.__log.debug('devs=%s', devs)

        self._devs = devs
        self._dc_mtr = dc_mtr

        self._obj = []
        for d in self._devs:
            self._obj.append(AbShutter(d, self.cb_func, debug=self._dbg))

        self._stop = True;
        self._rotate = False;

    def main(self):
        self.__log.debug('')
        
        for o in self._obj:
            o.start()

        while True:
            print(time.strftime('%Y/%m/%d(%a) %H:%M:%S'))
            time.sleep(5)

    def cb_func(self, dev, code, value):
        """ callback function """
        self.__log.debug('dev=%d, code=%d:%s, value=%d:%s', 
                         dev,
                         code, AbShutter.keycode2str(code),
                         value, AbShutter.keyval2str(value))

        if AbShutter.keyval2str(value) in ['RELEASE']:
            return

        if AbShutter.keycode2str(code) in ['KEY_ENTER']:
            self._stop = not self._stop

        if AbShutter.keycode2str(code) in ['KEY_VOLUMEUP']:
            if self._stop:
                return

            self._rotate = not self._rotate

        if self._stop:
            self._dc_mtr.send_cmdline('stop')
            self._rotate = False
            return

        if self._rotate:
            self._dc_mtr.send_cmdline('speed 50 -50')
        else:
            self._dc_mtr.send_cmdline('speed 50 50')
            return


@click.command(help="ab_shutter")
@click.argument('devs', metavar='[0|1|2|4..]...', type=int, nargs=-1)
@click.option('--svr_host', '-s', 'svr_host', type=str, default='localhost',
              help='server hostname')
@click.option('--svr_port', '-p', 'svr_port', type=int, default=12345,
              help='server port number')
@click.option('--debug', '-d', 'debug', is_flag=True, default=False,
              help='debug flag')
@click.pass_obj
def dc_mtr(obj, devs, svr_host, svr_port, debug):
    """ ab_shutter """
    __log = get_logger(__name__, obj['debug'] or debug)
    __log.debug('obj=%s, devs=%s', obj, devs)

    dc_mtr = DcMtrClient(svr_host, svr_port, obj['debug'] or debug)
    test_app = Test_DcMtr(devs, dc_mtr, obj['debug'] or debug)

    try:
        test_app.main()

    finally:
        dc_mtr.send_cmdline('stop')
        print('END')
