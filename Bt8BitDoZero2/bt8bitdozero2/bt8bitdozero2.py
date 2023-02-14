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


class Bt8BitDoZero2(threading.Thread):
    EV_KEY_VAL = ('RELEASE', 'PUSH', 'HOLD')
    EV_ABS_VAL = ('LOW', 'MIDDLE', 'HIGHT')  # int(value/127)
    DEVFILE_PREFIX = '/dev/input/event'

    def __init__(self, dev=0, cb_func=None, debug=False):
        self._dbg = debug
        __class__.__log = get_logger(__class__.__name__, self._dbg)
        self.__log.debug('dev=%d', dev)

        self.dev = dev
        self.cb_func = cb_func
        
        self.input_dev_file = self.DEVFILE_PREFIX + str(self.dev)
        self.__log.debug('input_dev_file=%s', self.input_dev_file)

        self.input_dev = evdev.device.InputDevice(self.input_dev_file)

        super().__init__(daemon=True)

    def wait_key_event(self):
        self.__log.debug('%s', self.input_dev_file)
        
        for ev in self.input_dev.read_loop():
            if ev.type in [evdev.events.EV_KEY, evdev.events.EV_ABS]:
                break

            self.__log.debug('ignore: %s', ev)

        self.__log.debug('(ev.type, ev.code, ev.value)=%s',
                         (ev.type, ev.code, ev.value))

        if self.cb_func != None:
            self.cb_func(self.dev, ev.type, ev.code, ev.value)

        return (ev.type, ev.code, ev.value)

    def run(self):
        self.__log.debug('')

        flag_err = False
        while True:
            try:
                self.input_dev = evdev.device.InputDevice(self.input_dev_file)
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

    @classmethod
    def keycode2str(cls, evtype, code):
        strlist = evdev.ecodes.bytype[evtype][code]
        return evdev.ecodes.bytype[evtype][code]

    @classmethod
    def keyval2str(cls, evtype, value):
        if evtype == evdev.events.EV_ABS:
            return cls.EV_ABS_VAL[int(value/127)]

        return cls.EV_KEY_VAL[value]