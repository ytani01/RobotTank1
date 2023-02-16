#!/usr/bin/env python3
#
# Copyright (c) 2023 Yoichi Tanibayashi
#
# -*- coding: utf-8 -*-
#
import click
import time
# import datetime
import random
import threading
from enum import Enum
from dcmtr import DcMtrClient
from bt8bitdozero2 import Bt8BitDoZero2
from .my_logger import get_logger
from . import DistanceVL53L0X


class Direction(Enum):
    STOP = 0
    FORWARD = 1
    BACKWARD = 2
    LEFT = 3
    RIGHT = 4
    NULL = -1


class SensorWatcher(threading.Thread):
    """   """

    DISTANCE_MAX = 600
    DISTANCE_NEAR = 200

    def __init__(self, dc_mtr, sensor, debug=False):
        self._dbg = debug
        __class__.__log = get_logger(__class__.__name__, self._dbg)
        self.__log.debug('')

        self._dc_mtr = dc_mtr
        self._sensor = sensor

        self._active = False

        self._auto = True

        super().__init__(daemon=True)

    def end(self):
        self.__log.debug('')
        self._active = False
        self.join()
        self.__log.debug('END')

    def auto_on(self):
        self._auto = True

    def auto_off(self):
        self._auto = False

    def run(self):
        self.__log.debug('')

        self._active = True

        while self._active:
            if not self._auto:
                time.sleep(1)
                continue

            distance = self._sensor.get_distance()
            if distance is None:
                self._dc_mtr.send_cmdline('clear')
                self._dc_mtr.send_cmdline('speed 0 0')
                time.sleep(1)
                continue

            self.__log.info('distance=%s', distance)

            if distance <= self.DISTANCE_NEAR:
                self._dc_mtr.send_cmdline('clear')
                self._dc_mtr.send_cmdline('speed 0 0')
                self._dc_mtr.send_cmdline('delay 0.1')
                self._dc_mtr.send_cmdline('speed -60 -60')
                self._dc_mtr.send_cmdline('delay 0.5')
                if random.random() > 0.5:
                    self._dc_mtr.send_cmdline('speed 60 0')
                else:
                    self._dc_mtr.send_cmdline('speed 0 60')
                self._dc_mtr.send_cmdline('delay %s' % (1 + random.random()))

                time.sleep(1.5)

            time.sleep(self._sensor.get_timing())

        self._sensor.end()


class Test_RobotTankAuto:
    """ Test RobotTankAuto class """

    SPEED_MAX = 100
    DEF_BASE_SPEED = 60

    def __init__(self, interval=1, dc_mtr=None, debug=False):
        self._dbg = debug
        __class__.__log = get_logger(__class__.__name__, self._dbg)
        self.__log.debug('interval=%s', interval)

        self._interval = interval
        self._dc_mtr = dc_mtr

        self._sensor = DistanceVL53L0X(debug=self._dbg)

        self._watcher = SensorWatcher(
            self._dc_mtr, self._sensor, debug=self._dbg)

        self._dir = Direction.LEFT
        self._base_speed = self.DEF_BASE_SPEED

    def main(self):
        self.__log.debug('')

        self._sensor.start()
        self._sensor.wait_active()

        self._watcher.start()

        if self._interval <= 0.0:
            self._interval = self._sensor.get_timing()
            self.__log.debug('interval=%s', self._interval)

        try:
            while True:
                cmdline = 'speed 0 0'

                if self._dir == Direction.LEFT:
                    cmdline = 'speed 0 %s' % (self._base_speed)
                    self._dir = Direction.RIGHT

                else:
                    cmdline = 'speed %s 0' % (self._base_speed)
                    self._dir = Direction.LEFT

                self._dc_mtr.send_cmdline(cmdline)

                time.sleep(0.5 + random.random())

        except KeyboardInterrupt as e:
            self.__log.warning('%s:%s', type(e).__name__, e)

        except Exception as e:
            self.__log.error('%s:%s', type(e).__name__, e)

        self._dc_mtr.send_cmdline('speed 0 0')
        self._watcher.end()


@click.command(help="Robot Tank Auto Pilot Test")
@click.argument('interval', metavar='interval[sec]', type=float)
@click.option('--svr_host', '-s', 'svr_host', type=str, default='localhost',
              help='server hostname')
@click.option('--svr_port', '-p', 'svr_port', type=int, default=12345,
              help='server port number')
@click.option('--debug', '-d', 'debug', is_flag=True, default=False,
              help='debug flag')
@click.pass_obj
def robottankauto(obj, interval, svr_host, svr_port, debug):
    """ robottankauto """
    __log = get_logger(__name__, obj['debug'] or debug)
    __log.debug('obj=%s, interval=%s, svr=%s',
                obj, interval, (svr_host, svr_port))

    dc_mtr = DcMtrClient(svr_host, svr_port, obj['debug'] or debug)
    test_app = Test_RobotTankAuto(
        interval, dc_mtr, debug=obj['debug'] or debug)

    try:
        test_app.main()

    finally:
        __log.info('END')
