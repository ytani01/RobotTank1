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
    """ Direction """
    STOP = 0
    FORWARD = 1
    BACKWARD = 2
    LEFT = 3
    RIGHT = 4
    NULL = -1


class SensorWatcher(threading.Thread):
    """ Sensor Watcher  """

    DISTANCE_MAX = 600
    DISTANCE_NEAR = 200

    def __init__(self, dc_mtr, base_speed, sensor, debug=False):
        """
        Parameters
        ----------
        dc_mtr: DcMtrClient
        base_speed: int
        sensor: DistanceVL53L0X
        """
        self._dbg = debug
        __class__.__log = get_logger(__class__.__name__, self._dbg)
        self.__log.debug('base_speed=%s', base_speed)

        self._dc_mtr = dc_mtr
        self._base_speed = base_speed
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

            if distance < self.DISTANCE_NEAR or distance > self.DISTANCE_MAX:
                self.__log.info('distance=%s !!', distance)

                self._dc_mtr.send_cmdline('clear')

                self._dc_mtr.send_cmdline('speed 0 0')
                self._dc_mtr.send_cmdline('delay 0.1')

                self._dc_mtr.send_cmdline('speed %s %s' % (
                    -self._base_speed, -self._base_speed))
                self._dc_mtr.send_cmdline('delay %s' % (0.2 + random.random()))

                if random.random() > 0.5:
                    self._dc_mtr.send_cmdline('speed %s 0' % (self._base_speed))
                else:
                    self._dc_mtr.send_cmdline('speed 0 %s' % (self._base_speed))

                self._dc_mtr.send_cmdline('delay %s' % (0.5 + random.random()))

                time.sleep(1.5)

            time.sleep(self._sensor.get_timing())

        self._sensor.end()


class Test_RobotTankAuto:
    """ Test RobotTankAuto class """

    SPEED_MAX = 100
    DEF_BASE_SPEED = 70

    def __init__(self, offset=0.0, interval=0.0, dc_mtr=None, debug=False):
        """
        Parameters
        ----------
        offset: float
        interval: float
        dc_mtr: DcMtrclient
        """
        self._dbg = debug
        __class__.__log = get_logger(__class__.__name__, self._dbg)
        self.__log.debug('offset=%s, interval=%s', offset, interval)

        self._offset = offset
        self._interval = interval
        self._dc_mtr = dc_mtr

        self._dir = Direction.LEFT
        self._base_speed = self.DEF_BASE_SPEED

        self._sensor = DistanceVL53L0X(offset=self._offset, debug=self._dbg)

        self._watcher = SensorWatcher(
            self._dc_mtr, self._base_speed, self._sensor, debug=self._dbg)

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
                    cmdline = 'speed %s %s' % (
                        int(self._base_speed / 4), self._base_speed)
                    self._dir = Direction.RIGHT

                else:
                    cmdline = 'speed %s %s' % (
                        self._base_speed, int(self._base_speed / 4))
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
@click.option('--offset', '-o', 'offset', type=float, default=0.0,
              help='distance sensor offset (mm)')
@click.option('--interval', '-i', 'interval', type=float, default=0.0,
              help='interval sec')
@click.option('--svr_host', '-s', 'svr_host', type=str, default='localhost',
              help='server hostname')
@click.option('--svr_port', '-p', 'svr_port', type=int, default=12345,
              help='server port number')
@click.option('--debug', '-d', 'debug', is_flag=True, default=False,
              help='debug flag')
@click.pass_obj
def robottankauto(obj, offset, interval, svr_host, svr_port, debug):
    """ robottankauto """
    __log = get_logger(__name__, obj['debug'] or debug)
    __log.debug('obj=%s', obj)
    __log.debug('offset=%s, interval=%s, svr=%s',
                offset, interval, (svr_host, svr_port))

    dc_mtr = DcMtrClient(svr_host, svr_port, obj['debug'] or debug)

    test_app = Test_RobotTankAuto(
        offset, interval, dc_mtr, debug=obj['debug'] or debug)
    try:
        test_app.main()

    finally:
        __log.info('END')
