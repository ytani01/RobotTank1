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


class BtKbd(threading.Thread):
    EV_VAL = ('RELEASE', 'PUSH', 'HOLD')
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
            self.__log.debug(ev)
            if ev.type == evdev.events.EV_KEY:
                break
            self.__log.debug('ignore this event')

        self.__log.debug('(ev.code, ev.value)=%s', (ev.code, ev.value))

        if self.cb_func != None:
            self.cb_func(self.dev, ev.code, ev.value)

        return (ev.code, ev.value)

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
                (code, value) = self.wait_key_event()
            except Exception as e:
                flag_err = True
                self.__log.error('%s:%s', type(e).__name__, e)
                time.sleep(2)
                continue
            else:
                if flag_err:
                    flag_err = False
                    self.__log.info('Connected: %s', self.input_dev_file)

            self.__log.debug('%s(%d) %s(%d)',
                             __class__.keycode2str(code), code, 
                             __class__.keyval2str(value), value)

    @classmethod
    def keycode2str(cls, code):
        return evdev.events.keys[code]

    @classmethod
    def keyval2str(cls, value):
        return cls.EV_VAL[value]
