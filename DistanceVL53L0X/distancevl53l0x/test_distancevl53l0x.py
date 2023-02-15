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
from . import DistanceVL53L0X


class Test_DistanceVL53L0X:
    """ Test DistanceVL53L0X class """

    def __init__(self, devs, debug=False):
        self._dbg = debug
        __class__.__log = get_logger(__class__.__name__, self._dbg)
        self.__log.debug('devs=%s', devs)

        self._devs = devs

        self._distancevl53l0x = []
        for d in self._devs:
            distancevl53l0x = None
            while distancevl53l0x is None:
                try:
                    distancevl53l0x = DistanceVL53L0X(
                        d, self.cb_func, debug=self._dbg)
                except Exception as e:
                    self.__log.error('%s:%s', type(e).__name__, e)
                    time.sleep(2)
                else:
                    self.__log.info('Connected: %s', d)

            self._distancevl53l0x.append(distancevl53l0x)

    def main(self):
        self.__log.debug('')

        for distancevl53l0x in self._distancevl53l0x:
            distancevl53l0x.start()

        while True:
            print(time.strftime('%Y/%m/%d(%a) %H:%M:%S'))
            time.sleep(5)

    def cb_func(self, dev, evtype, code, value):
        """ callback function """
        self.__log.info('dev=%d, evtype=%d:%s, code=%d:%s, value=%d:%s',
                        dev, evtype, evdev.ecodes.EV[evtype], 
                        code, DistanceVL53L0X.keycode2str(evtype, code),
                        value, DistanceVL53L0X.keyval2str(evtype, value))


@click.command(help="VL53L0X Distance Sensor Test")
@click.argument('devs', metavar='dev_num[0|1|2|3..]...', type=int, nargs=-1)
@click.option('--debug', '-d', 'debug', is_flag=True, default=False,
              help='debug flag')
@click.pass_obj
def distancevl53l0x(obj, devs, debug):
    """ distancevl53l0x """
    __log = get_logger(__name__, obj['debug'] or debug)
    __log.debug('obj=%s, devs=%s', obj, devs)

    test_app = Test_DistanceVL53L0X(devs, obj['debug'] or debug)

    try:
        test_app.main()

    finally:
        print('END')
