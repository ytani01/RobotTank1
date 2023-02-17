#!/usr/bin/env python3
#
# Copyright (c) 2023 Yoichi Tanibayashi
#
# -*- coding: utf-8 -*-
#
import time
import threading
from .VL53L0X import VL53L0X, Vl53l0xAccuracyMode
from .my_logger import get_logger


class DistanceVl53l0xError(RuntimeError):
    pass


class DistanceVL53L0X(threading.Thread):
    """
    """
    DEF_I2C_BUS = 1
    DEF_I2C_ADDR = 0x29

    DISTANCE_MAX = 8190

    def __init__(self, offset=0.0,
                 i2c_bus=DEF_I2C_BUS, i2c_addr=DEF_I2C_ADDR,
                 mode=Vl53l0xAccuracyMode.LONG_RANGE,
                 debug=False):
        """
        Parameters
        ----------
        offset: float
        i2c_bus: int
        i2c_addr: int
        mode: Vl3l0xAccuracyMode
        """
        self._dbg = debug
        __class__.__log = get_logger(__class__.__name__, self._dbg)
        self.__log.debug('offset=%s, i2c:%d, 0x%X', offset, i2c_bus, i2c_addr)

        self._offset = offset
        self._i2c_bus = i2c_bus
        self._i2c_addr = i2c_addr
        self._mode = mode

        self._tof = VL53L0X(
            i2c_bus=self._i2c_bus, i2c_address=self._i2c_addr)

        self._timing = None
        self._distance = None
        self._active = False

        super().__init__(daemon=True)

    def _start(self):
        self._tof.open()

        self._tof.start_ranging(self._mode)

        self._timing = self._tof.get_timing()
        self.__log.debug('timing=%s', self._timing)

    def _end(self):
        self._tof.stop_ranging()
        self._tof.close()

    def end(self):
        self.__log.debug('')
        self._active = False
        self.join()
        self.__log.debug('END')

    def is_active(self):
        return self._active

    def get_timing(self):
        return self._timing / 1000000.0

    def wait_active(self, timelimit=5.0):
        self.__log.debug('timelimit=%s', timelimit)

        start_time = time.time()
        delay = 0.0

        while not self._active:
            delay = time.time() - start_time

            if delay >= timelimit:
                break

            time.sleep(0.1)

        self.__log.debug('Done: timelimit=%s', timelimit)
        return delay

    def get_distance(self):
        """ get_distance
        Returns
        -------
        distance: float
        """
        if not self._active:
            self.__log.warning('active=%s', self._active)
            return None

        self.__log.debug('distance=%s', self._distance)
        return self._distance

    def run(self):
        self.__log.debug('')

        self._start()

        self._active = True

        while self._active:
            try:
                self._distance = max(
                    0, self._tof.get_distance() + self._offset)

            except Exception as e:
                self.__log.error('%s:%s', type(e).__name__, e)
                self._active = False
                break

            time.sleep(self._timing / 1000000.0)

        self._end()
