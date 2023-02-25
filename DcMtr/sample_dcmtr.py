#!/usr/bin/env python3
#
# Copyright (c) 2023 Yoichi Tanibayashi
#
# -*- coding: utf-8 -*-
#
import sys
import time
import pigpio
import click
from dcmtr import DcMtr, get_logger


class App:
    def __init__(self, pi, pin, speed, debug=False):
        self._dbg = debug
        __class__.__log = get_logger(__class__.__name__, self._dbg)
        self.__log.debug('pin=%s', pin)

        self._pi = pi
        self._pin = pin
        self._speed = speed

        self._mtr = DcMtr(self._pi, self._pin, debug=self._dbg)

    def main(self):
        self.__log.debug('')

        self._mtr.set_speed(self._speed)
        time.sleep(0.5)
        self._mtr.set_break()
        time.sleep(0.5)
        self._mtr.set_speed(-self._speed)
        time.sleep(0.5)
        self._mtr.set_stop()


@click.command(context_settings=dict(help_option_names=['-h', '--help']),
               help='DcMtr Sample')
@click.argument('pin1', type=int, metavar='PIN1')
@click.argument('pin2', type=int, metavar='PIN2')
@click.argument('speed', type=int, metavar='SPEED')
@click.option('--debug', '-d', 'debug', is_flag=True, default=False,
              help='')
def main(pin1, pin2, speed, debug):
    __log = get_logger(__name__, debug)
    __log.debug('(pin1, pin2)=%s, speed=%s', (pin1, pin2), speed)

    pin = (pin1, pin2)

    res = 0
    pi = pigpio.pi()
    app = App(pi, pin, speed, debug)

    try:
        print('START')
        app.main()

    except KeyboardInterrupt as e:
        __log.info('%s', type(e).__name__)

    except Exception as e:
        __log.error('%s:%s', type(e).__name__, e)
        sys.exit(1)

    finally:
        pi.stop()
        print('END')
        sys.exit(res)

if __name__ == '__main__':
    main()
