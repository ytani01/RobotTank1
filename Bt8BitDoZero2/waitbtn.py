#!/usr/bin/env python3
#
# Copyright (c) 2023 Yoichi Tanibayashi
#
# -*- coding: utf-8 -*-
#
import sys
import time
import click
from bt8bitdozero2 import Bt8BitDoZero2, Bt8BitDoZero2N, get_logger


DEF_DEV = [0]


class App:
    def __init__(self, btn, dev, debug=False):
        self._dbg = debug
        __class__.__log = get_logger(__class__.__name__, self._dbg)
        self.__log.debug('btn=%s, dev=%s', btn, dev)

        self._btn = btn
        self._dev = dev

        if len(self._btn) == 0:
            self._btn = Bt8BitDoZero2.BTN.keys()
            self.__log.debug('btn=%s', self._btn)

        self._res = 1

        self._btkey = Bt8BitDoZero2N(self._dev, self.cb, self._dbg)

    def main(self):
        for b in self._btn:
            if b not in Bt8BitDoZero2.BTN.keys():
                self.__log.error('%a: Invalid Button', b)
                return self._res
            
        self._btkey.start()

        while self._res > 0:
            time.sleep(0.1)

        return self._res

    def cb(self, dev, evtype, code, value):
        self.__log.debug('%s', (dev, evtype, code, value))
        for b in self._btn:
            if Bt8BitDoZero2.pushed(b, evtype, code, value):
                print(b)
                self._res = 0


@click.command(context_settings=dict(help_option_names=['-h', '--help']),
               help='wait for a button to be pushed')
@click.argument('btn', type=str, nargs=-1,
                metavar='[A|B|X|Y|TL|TR|SEL|ST|UD|LR] ...')
@click.option('--dev', '-D', 'dev', type=int, default=DEF_DEV, multiple=True,
              help='device number (default=%s)' % (DEF_DEV))
@click.option('--debug', '-d', 'debug', is_flag=True, default=False,
              help='debug flag')
def main(btn, dev, debug):
    __log = get_logger(__name__, debug)
    __log.debug('btn=%s, dev=%s', btn, dev)

    res = 1
    app = App(btn, dev, debug)

    try:
        res = app.main()
    except KeyboardInterrupt as e:
        __log.info('%s', type(e).__name__)
        res = 0
    except Exception as e:
        __log.error('%s:%s', type(e).__name__, e)
        res = 2
    finally:
        __log.debug('res=%s', res)
        sys.exit(res)


if __name__ == '__main__':
    main()
