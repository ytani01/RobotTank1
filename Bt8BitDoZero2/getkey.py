#!/usr/bin/env python3
#
# Copyright (c) 2023 Yoichi Tanibayashi
#
# -*- coding: utf-8 -*-
#
import os
import time
import click
from bt8bitdozero2 import Bt8BitDoZero2, Bt8BitDoZero2N, get_logger


class App:
    def __init__(self, keys, devs, debug=False):
        self._dbg = debug
        __class__.__log = get_logger(__class__.__name__, self._dbg)
        self.__log.debug('keys=%s, devs=%s', keys, devs)

        self._keys = keys
        self._devs = devs

        self._btkey = Bt8BitDoZero2N(self._devs, self.cb, self._dbg)

    def main(self):
        self._btkey.start()

        while True:
            time.sleep(5)

    def cb(self, dev, evtype, code, value):
        idx = 0
        for k in self._keys:
            if Bt8BitDoZero2.pushed(k, evtype, code, value):
                print(idx)
                os._exit(0)
            idx += 1


@click.command(context_settings=dict(help_option_names=['-h', '--help']),
               help='get key')
@click.argument('keys', type=str, nargs=-1,
                metavar='[A|B|X|Y|TL|TR|SEL|ST|UD|LR] ...')
@click.option('--dev', '-v', 'devs', type=int, default=[0],
              multiple=True,
              help='delay sec (default: %s)' % (0))
@click.option('--debug', '-d', 'debug', is_flag=True, default=False,
              help='')
def main(keys, devs, debug):
    __log = get_logger(__name__, debug)
    __log.debug('keys=%s, devs=%s', keys, devs)

    app = App(keys, devs, debug)

    try:
        app.main()
    except Exception as e:
        __log.error('%s:%s', type(e).__name__, e)
    finally:
        pass


if __name__ == '__main__':
    main()
