#!/usr/bin/env python3
#
# Copyright (c) 2023 Yoichi Tanibayashi
#
# -*- coding: utf-8 -*-
#
import evdev
import time
import threading
from .my_logger import get_logger


class Bt8BitDoZero2N:
    """  """
    def __init__(self, devs=[], cb_func=None, debug=False):
        """
        Parameters
        ----------
        devs: list(Bt8BitDoZero2)
        cb_func: lambda()
        """
        self._dbg = debug
        __class__.__log = get_logger(__class__.__name__, self._dbg)
        self.__log.debug('devs=%s', devs)

        self._devs = devs
        self._cb_func = cb_func

        self._bt8bitdozero2 = []

    def start(self):
        for d in self._devs:
            b = None
            while b is None:
                try:
                    b = Bt8BitDoZero2(
                        d, self._cb_func, debug=self._dbg)
                except Exception as e:
                    self.__log.error('%s:%s', type(e).__name__, e)
                    time.sleep(2)
                else:
                    self.__log.debug('connect: %s', d)

            self._bt8bitdozero2.append(b)

        for b in self._bt8bitdozero2:
            b.start()


class Bt8BitDoZero2(threading.Thread):
    DEVFILE_PREFIX = '/dev/input/event'

    EV_KEY_VAL = ('RELEASE', 'PUSH', 'HOLD')
    EV_ABS_VAL = ('LOW', 'MIDDLE', 'HIGH')  # int(value/127)

    BTN = {
        'A': [1, 304],
        'B': [1, 305],
        'X': [1, 307],
        'Y': [1, 308],
        'UD': [3, 1],
        'LR': [3, 0],
        'TL': [1, 310],
        'TR': [1, 311],
        'SEL': [1, 314],
        'ST': [1, 315]
    }

    def __init__(self, dev=0, cb_func=None, debug=False):
        """
        Parameters
        ----------
        dev : int
        cb_func : func
        debug : bool
        """
        self._dbg = debug
        __class__.__log = get_logger(__class__.__name__, self._dbg)
        self.__log.debug('dev=%d', dev)

        self.dev = dev
        self.cb_func = cb_func

        self.input_dev_file = self.DEVFILE_PREFIX + str(self.dev)
        self.__log.debug('input_dev_file=%s', self.input_dev_file)

        self.input_dev = evdev.device.InputDevice(self.input_dev_file)

        self._active = False

        super().__init__(daemon=True)

    def wait_key_event(self):
        """
        キーイベントを待つ
        """
        self.__log.debug('%s', self.input_dev_file)

        try:
            for ev in self.input_dev.read_loop():
                if ev.type in [evdev.events.EV_KEY, evdev.events.EV_ABS]:
                    break

                self.__log.debug('ignore: %s', ev)

        except Exception as e:
            self.__log.error('%s:%s', type(e).__name__, e)

        self.__log.debug('(ev.type, ev.code, ev.value)=%s',
                         (ev.type, ev.code, ev.value))

        if self.cb_func is not None:
            self.__log.debug(self.cb_func)
            self.cb_func(self.dev, ev.type, ev.code, ev.value)

        return (ev.type, ev.code, ev.value)

    def run(self):
        self.__log.debug('')

        self._active = True
        flag_err = False

        while self._active:
            try:
                self.input_dev = evdev.device.InputDevice(
                    self.input_dev_file)
            except Exception as e:
                flag_err = True
                self.__log.error('%s:%s', type(e).__name__, e)
                time.sleep(2)
                continue
            else:
                if flag_err:
                    flag_err = False
                    self.__log.info('Connected: %s', self.input_dev_file)

            try:
                (evtype, code, value) = self.wait_key_event()
            except Exception as e:
                flag_err = True
                self.__log.error('%s:%s', type(e).__name__, e)
                time.sleep(2)
                continue
            else:
                if flag_err:
                    flag_err = False
                    self.__log.info('Connected: %s', self.input_dev_file)

            self.__log.debug('%s(%d) %s(%d) %s(%d)',
                             evdev.ecodes.EV[evtype], evtype,
                             __class__.keycode2str(evtype, code), code,
                             __class__.keyval2str(evtype, value), value)

            self.input_dev.close()

        self.__log.debug('END')

    @classmethod
    def keycode2str(cls, evtype, code):
        return evdev.ecodes.bytype[evtype][code]

    @classmethod
    def keyval2str(cls, evtype, value):
        if evtype == evdev.events.EV_ABS:
            return cls.EV_ABS_VAL[int(value/127)]

        return cls.EV_KEY_VAL[value]

    @classmethod
    def pushed(cls, btn_name, evtype, code, val):
        if cls.keyval2str(evtype, val) != 'PUSH':
            return False

        if [evtype, code] == cls.BTN[btn_name]:
            return True

        return False
