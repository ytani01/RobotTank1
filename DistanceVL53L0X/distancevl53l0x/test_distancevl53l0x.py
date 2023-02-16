#!/usr/bin/env python3
#
# Copyright (c) 2023 Yoichi Tanibayashi
#
# -*- coding: utf-8 -*-
#
import click
import time
import datetime
from .my_logger import get_logger
from . import DistanceVL53L0X


class Test_DistanceVL53L0X:
    """ Test DistanceVL53L0X class """

    DISTANCE_MAX = 500

    def __init__(self, interval=1, debug=False):
        self._dbg = debug
        __class__.__log = get_logger(__class__.__name__, self._dbg)
        self.__log.debug('interval=%s', interval)

        self._interval = interval

        self._distancevl53l0x = DistanceVL53L0X(debug=self._dbg)

    def main(self):
        self.__log.debug('')

        self._distancevl53l0x.start()
        self._distancevl53l0x.wait_active()

        if self._interval <= 0.0:
            self._interval = self._distancevl53l0x.get_timing()
            self.__log.debug('interval=%s', self._interval)

        try:
            while True:
                distance = self._distancevl53l0x.get_distance()
                if distance is None:
                    time.sleep(self._interval)
                    continue

                distance_graph = '*' * int(distance / 10.0)
                if distance > self.DISTANCE_MAX:
                    distance_graph = '*' * int(self.DISTANCE_MAX / 10) + '!'

                tm = datetime.datetime.now().strftime(
                    '%Y/%m/%d(%a) %H:%M:%S.%f')
                print('%s %4d mm %s' % (tm, distance, distance_graph))

                time.sleep(self._interval)

        except KeyboardInterrupt as e:
            self.__log.warning('%s:%s', type(e).__name__, e)

        except Exception as e:
            self.__log.error('%s:%s', type(e).__name__, e)

        self._distancevl53l0x.end()


@click.command(help="VL53L0X Distance Sensor Test")
@click.argument('interval', metavar='interval[sec]', type=float)
@click.option('--debug', '-d', 'debug', is_flag=True, default=False,
              help='debug flag')
@click.pass_obj
def distance(obj, interval, debug):
    """ distancevl53l0x """
    __log = get_logger(__name__, obj['debug'] or debug)
    __log.debug('obj=%s, interval=%s', obj, interval)

    test_app = Test_DistanceVL53L0X(interval, debug=obj['debug'] or debug)

    try:
        test_app.main()

    finally:
        __log.info('END')
