#!/usr/bin/env python3
#
# Copyright (c) 2023 Yoichi Tanibayashi
#
# -*- coding: utf-8 -*-
#
import click
import time
from enum import Enum, auto
from dcmtr import DcMtrClient
from .my_logger import get_logger
from . import AbShutter


class Move(Enum):
    STOP = auto()
    FORWARD = auto()
    BACKWARD = auto()
    ROTATE_LEFT = auto()
    ROTATE_RIGHT = auto()


class Test_DcMtr:
    """ Test AbShutter class """

    FWD_SPEED = 60
    ROT_SPEED = 30

    def __init__(self, devs, dc_mtr, debug=False):
        self._dbg = debug
        __class__.__log = get_logger(__class__.__name__, self._dbg)
        self.__log.debug('devs=%s', devs)

        self._devs = devs
        self._dc_mtr = dc_mtr

        self._obj = []
        for d in self._devs:
            o = None
            while o is None:
                try:
                    o = AbShutter(d, self.cb_func, debug=self._dbg)
                except Exception as e:
                    self.__log.error('%s:%s', type(e).__name__, e)
                    time.sleep(2)
                else:
                    self.__log.info('connect: %s', d)

            self._obj.append(o)

        self._move = Move.STOP
        self._key_push = False

    def main(self):
        self.__log.debug('')

        for o in self._obj:
            o.start()

        while True:
            self.__log.debug(time.strftime('%Y/%m/%d(%a) %H:%M:%S'))
            time.sleep(5)

    def cb_func(self, dev, code, value):
        """ callback function """
        self.__log.info('dev=%d, code=%d:%s, value=%d:%s',
                         dev,
                         code, AbShutter.keycode2str(code),
                         value, AbShutter.keyval2str(value))

        if self._key_push:
            if AbShutter.keyval2str(value) not in ['RELEASE']:
                return

            if AbShutter.keycode2str(code) not in ['KEY_VOLUMEUP']:
                return

            self._key_push = False
            return

        # self._key_push == False

        if AbShutter.keyval2str(value) in ['RELEASE']:
            return

        self._key_push = True

        if AbShutter.keycode2str(code) in ['KEY_ENTER']:
            if self._move == Move.STOP:
                self._move = Move.ROTATE_RIGHT
            else:
                self._move = Move.STOP

        if AbShutter.keycode2str(code) in ['KEY_VOLUMEUP']:
            if self._move == Move.FORWARD:
                self._move = Move.ROTATE_LEFT
            else:
                self._move = Move.FORWARD

        # move
        if self._move == Move.STOP:
            self._dc_mtr.send_cmdline('stop')
            self._rotate = True
            return

        if self._move == Move.FORWARD:
            self._dc_mtr.send_cmdline('speed %s %s' %
                                      (self.FWD_SPEED, self.FWD_SPEED))
            return

        if self._move == Move.ROTATE_LEFT:
            self._dc_mtr.send_cmdline('speed %s %s' %
                                      (-self.ROT_SPEED, self.ROT_SPEED))
            return

        if self._move == Move.ROTATE_RIGHT:
            self._dc_mtr.send_cmdline('speed %s %s' %
                                      (self.ROT_SPEED, -self.ROT_SPEED))
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
