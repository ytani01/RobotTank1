#!/usr/bin/env python3
#
# Copyright (c) 2023 Yoichi Tanibayashi
#
# -*- coding: utf-8 -*-
#
import sys
import click
import time
# import datetime
import random
import threading
from enum import Enum
from cmdclientserver import CmdClient
from bt8bitdozero2 import Bt8BitDoZero2, Bt8BitDoZero2N
from distancevl53l0x import DistanceClient, get_logger


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

    DEF_DISTANCE_NEAR = 120
    DISTANCE_TOO_NEAR = 50
    DISTANCE_FAR = 600
    DISTANCE_MAX = 8190.0

    def __init__(self, dc_mtr, base_speed, distance_client, debug=False):
        """
        Parameters
        ----------
        dc_mtr: CmdClient
        base_speed: int
        distance_client: DistanceClient
        """
        self._dbg = debug
        __class__.__log = get_logger(__class__.__name__, self._dbg)
        self.__log.debug('base_speed=%s', base_speed)

        self._dc_mtr = dc_mtr
        self._base_speed = base_speed
        self._d_clnt = distance_client

        self._active = False
        self._auto = False
        self._distance_near = self.DEF_DISTANCE_NEAR

        super().__init__(daemon=True)

    def end(self):
        self.__log.debug('')
        self._active = False
        self.join()
        self.__log.debug('END')

    def is_auto(self):
        return self._auto

    def toggle_auto(self):
        if self._auto:
            self.auto_off()
        else:
            self.auto_on()

    def auto_on(self):
        self._auto = True

    def auto_off(self):
        self._auto = False

    def run(self):
        self.__log.debug('')

        self._active = True

        near_count = 0

        while self._active:
            if not self.is_auto():
                time.sleep(0.5)
                continue

            speed = self._base_speed

            distance = self._d_clnt.get_distance()
            self.__log.info('distance=%s', distance)

            if distance is None:
                self._dc_mtr.call('CLEAR')
                self._dc_mtr.call('STOP')
                time.sleep(1)
                continue

            if distance < 0.0:
                self._dc_mtr.call('CLEAR')
                self._dc_mtr.call('STOP')
                time.sleep(0.5)
                continue

            if distance >= self.DISTANCE_MAX:
                time.sleep(0.1)
                continue

            if self._distance_near < distance <= self._distance_near * 1.1:
                if near_count == 0:
                    self.__log.info('[%d]%03dmm(%s,%s) !',
                                    near_count, int(distance),
                                    self._distance_near, self.DISTANCE_FAR)

                    self._dc_mtr.call('CLEAR')
                    self._dc_mtr.call('STOP')

                    delay1 = 0.2
                    self._dc_mtr.call('DELAY %s' % (delay1))
                    time.sleep(delay1)

                    near_count += 1
                    continue

                time.sleep(0.2)
                continue

            if (distance <= self._distance_near or
                distance >= self.DISTANCE_FAR):

                self.__log.info('[%d]%03dmm(%s,%s) !',
                                near_count, int(distance),
                                self._distance_near, self.DISTANCE_FAR)

                self._dc_mtr.call('CLEAR')
                self._dc_mtr.call('STOP')

                delay1 = 0.2
                self._dc_mtr.call('DELAY %s' % (delay1))
                time.sleep(delay1)

                if near_count < 2:
                    near_count += 1
                    continue

                near_count = 0

                # back
                self._dc_mtr.call('SPEED %s %s' % (-speed, -speed))

                delay2 = 0.3 + random.random() / 2
                self._dc_mtr.call('DELAY %s' % (delay2))

                # turn
                turn_speed = int(speed / 2)
                if random.random() >= 0.4:
                    self._dc_mtr.call(
                        'SPEED %s %s' % (turn_speed, -turn_speed))
                else:
                    self._dc_mtr.call(
                        'SPEED %s %s' % (-turn_speed, turn_speed))

                delay3 = 0.5 + random.random() * 2.0
                self._dc_mtr.call('DELAY %s' % (delay3))
                self.__log.info('delay3=%s', delay3)

                time.sleep(delay1 + delay2 + delay3)

            near_count = 0
            time.sleep(0.001)

        self._dc_mtr.call('STOP')


class RobotTankAuto:
    """ Robot Tank Auto Pilot """

    SPEED_MAX = 100
    DEF_BASE_SPEED = 70

    def __init__(self, devs=[], offset=0.0, interval=0.0,
                 dc_mtr=None, distance_client=None,
                 debug=False):
        """
        Parameters
        ----------
        offset: float
        interval: float
        dc_mtr: DcMtrclient
        distance_client: DistanceClient
        devs: list()
        """
        self._dbg = debug
        __class__.__log = get_logger(__class__.__name__, self._dbg)
        self.__log.debug('devs=%s, offset=%s, interval=%s',
                         devs, offset, interval)

        self._devs = devs
        self._offset = offset
        self._interval = interval
        self._dc_mtr = dc_mtr
        self._d_clnt = distance_client

        self._dir = Direction.LEFT
        self._base_speed = self.DEF_BASE_SPEED
        self._auto = False
        self._prev_auto = False

        self._watcher = SensorWatcher(
            self._dc_mtr, self._base_speed, self._d_clnt, debug=self._dbg)

        self._bt8bitdozero2 = Bt8BitDoZero2N(
            self._devs, self.btn_cb, debug=self._dbg)

    def main(self):
        self._watcher.start()

        self._bt8bitdozero2.start()

        if self._interval <= 0.0:
            self._interval = 0.01
            self.__log.debug('interval=%s', self._interval)

        self.__log.info('READY')

        try:
            while True:
                if not self.is_auto():
                    self.__log.debug('auto=%s', self._auto)
                    time.sleep(1)
                    continue

                cmdline = 'SPEED 0 0'

                if self._dir == Direction.LEFT:
                    cmdline = 'SPEED %s %s' % (
                        int(self._base_speed / 3), self._base_speed)
                    self._dir = Direction.RIGHT
                else:
                    cmdline = 'SPEED %s %s' % (
                        self._base_speed, int(self._base_speed / 3))
                    self._dir = Direction.LEFT

                self._dc_mtr.call(cmdline)

                time.sleep(.7 + random.random())

        except KeyboardInterrupt as e:
            self.__log.warning('%s:%s', type(e).__name__, e)

        except Exception as e:
            self.__log.error('%s:%s', type(e).__name__, e)

        self._dc_mtr.call('CLEAR')
        self._dc_mtr.call('SPEED 0 0')
        self._watcher.end()

    def btn_cb(self, dev, evtype, code, val):
        """  """
        self.__log.debug('')

        # !! code_strがlistのこともある !!
        evtype_str = Bt8BitDoZero2.evtype2str(evtype)
        code_str = Bt8BitDoZero2.keycode2str(evtype, code)
        val_str = Bt8BitDoZero2.keyval2str(evtype, val)

        self.__log.info('%d:%s(%d):%s(%d):%s(%d)',
                        dev, evtype_str, evtype, code_str, code, val_str, val)

        if val_str in ['RELEASE', 'MIDDLE']:
            return

        if not self.is_auto():
            if Bt8BitDoZero2.pushed('SEL', evtype, code, val):
                self._dc_mtr.call('CLEAR')
                self._dc_mtr.call('SPEED 0 0')
                self.auto_on()
            return

        # AUTO ON

        
        if Bt8BitDoZero2.pushed('A', evtype, code, val):
            self.auto_off()
            return

        if Bt8BitDoZero2.pushed('B', evtype, code, val):
            self.auto_off()
            return

        if Bt8BitDoZero2.pushed('X', evtype, code, val):
            self.auto_off()
            return

        if Bt8BitDoZero2.pushed('Y', evtype, code, val):
            self.auto_off()
            return

        if Bt8BitDoZero2.pushed('SEL', evtype, code, val):
            self.auto_off()
            return

        if Bt8BitDoZero2.pushed('LR', evtype, code, val) and val_str == 'HIGH':
            self._watcher._distance_near = max(
                self._watcher._distance_near - 5,
                self._watcher.DEF_DISTANCE_NEAR - 5 * 5)
            self.__log.info('distance_near=%s', self._watcher._distance_near)
            return

        if Bt8BitDoZero2.pushed('LR', evtype, code, val) and val_str == 'LOW':
            self._watcher._distance_near = min(
                self._watcher._distance_near + 5,
                self._watcher.DEF_DISTANCE_NEAR + 5 * 5)
            self.__log.info('distance_near=%s', self._watcher._distance_near)
            return


    def is_auto(self):
        return self._auto

    def auto_on(self):
        self.__log.info('')
        self._auto = True
        self._watcher.auto_on()

    def auto_off(self):
        self.__log.info('')
        self._auto = False
        self._watcher.auto_off()


@click.command(help="Robot Tank Auto Pilot")
@click.argument('devs', metavar='dev_num[0|1|2|4..]...', type=int, nargs=-1)
@click.option('--offset', '-o', 'offset', type=float, default=0.0,
              help='distance sensor offset (mm)')
@click.option('--interval', '-i', 'interval', type=float, default=0.0,
              help='interval sec')
@click.option('--dc_host', '--dcs', 'dc_host', type=str, default='localhost',
              help='DC Motor server hostname')
@click.option('--dc_port', '--dcp', 'dc_port', type=int, default=12345,
              help='DC Motor server port number')
@click.option('--ds_host', '--dss', 'ds_host', type=str, default='localhost',
              help='DC Motor server hostname')
@click.option('--ds_port', '--dsp', 'ds_port', type=int, default=12347,
              help='DC Motor server port number')
@click.option('--debug', '-d', 'debug', is_flag=True, default=False,
              help='debug flag')
def main(devs, offset, interval, dc_host, dc_port, ds_host, ds_port, debug):
    __log = get_logger(__name__, debug)
    __log.debug('devs=%s, offset=%s, interval=%s, dc=%s, ds=%s',
                devs, offset, interval,
                (dc_host, dc_port), (ds_host, ds_port))


    if len(devs) == 0:
        sys.exit(1)

    motor_client = CmdClient(dc_host, dc_port, debug=debug)
    distance_client = DistanceClient(ds_host, ds_port, debug=debug)

    app = RobotTankAuto(
        devs, offset, interval, motor_client, distance_client,
        debug=debug)
    try:
        __log.info('START')
        motor_client.call('CLEAR')
        motor_client.call('STOP')
        app.main()

    finally:
        motor_client.call('CLEAR')
        motor_client.call('STOP')
        __log.info('END')
        sys.exit(0)


if __name__ == '__main__':
    main()
