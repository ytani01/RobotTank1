#!/usr/bin/env python3
#
# Copyright (c) 2023 Yoichi Tanibayashi
#
# -*- coding: utf-8 -*-
#
import sys
import click
import time
from bt8bitdozero2 import Bt8BitDoZero2, Bt8BitDoZero2N, get_logger


exit_code = 0


class App:
    def __init__(self, devs, debug=False):
        self._dbg = debug
        __class__.__log = get_logger(__class__.__name__, self._dbg)
        self.__log.debug('devs=%s', devs)

        self._devs = devs

        self._bt8 = Bt8BitDoZero2N(self._devs, self.cb, self._dbg)

    def main(self):
        self.__log.debug('')

        self._bt8.start()

        while True:
            time.sleep(5)

    def cb(self, dev, evtype, code, value):
        print('  event%d %d:%s %3d:%-7s %3d:%s' % (
            dev,
            evtype, Bt8BitDoZero2.evtype2str(evtype),
            value, Bt8BitDoZero2.keyval2str(evtype, value),
            code, Bt8BitDoZero2.keycode2str(evtype, code)))

        if Bt8BitDoZero2.pushed('A', evtype, code, value):
            print('Pushed A')

        if Bt8BitDoZero2.pushed('UD', evtype, code, value):
            print('Pushed UP or DOWN')


@click.command(help="Bt8BitDoZero2 Test")
@click.argument('devs', metavar='dev_num[0|1|2|3..]...', type=int, nargs=-1)
@click.option('--debug', '-d', 'debug', is_flag=True, default=False,
              help='debug flag')
def main(devs, debug):
    __log = get_logger(__name__, debug)
    __log.debug('devs=%s', devs)

    if len(devs) == 0:
        __log.error('devs=%s', devs)
        sys.exit(1)

    app = App(devs, debug=debug)

    try:
        print('START')
        app.main()

    except KeyboardInterrupt as e:
        print('\n', file=sys.stderr)
        __log.info('%s:%s', type(e).__name__, e)

    finally:
        print('\nEND')
        sys.exit(exit_code)


if __name__ == '__main__':
    main()
