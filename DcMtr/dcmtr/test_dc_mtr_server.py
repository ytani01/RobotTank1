#!/usr/bin/env python3
#
# Copyright (c) 2023 Yoichi Tanibayashi
#
# -*- coding: utf-8 -*-
#
import pigpio
import click
from .my_logger import get_logger
from . import DcMtrServer


class Test_DcMtrServer:
    def __init__(self, pi, pin, port, debug=False):
        self._dbg = debug
        __class__.__log = get_logger(__class__.__name__, self._dbg)
        self._pi = pi
        self._pin = pin
        self._port = port
        self.__log.debug('pin=%s, port=%s', self._pin, self._port)

        self._svr = DcMtrServer(
            self._pi, self._pin, self._port, debug=self._dbg)

    def main(self):
        self.__log.info('start server')

        try:
            self._svr.serve_forever()
        except ValueError as e:
            self.__log.error('port=%s: is in use (?)', self._port)
            self.__log.error('  %s:%s', type(e).__name__, e)
        except Exception as e:
            self.__log.error('%s:%s', type(e).__name__, e)
        except KeyboardInterrupt as e:
            self.__log.info('%s:%s', type(e).__name__, e)

        self.__log.debug('done')


@click.command(help="dc_mtr_server")
@click.argument('pin1', type=int)
@click.argument('pin2', type=int)
@click.argument('pin3', type=int)
@click.argument('pin4', type=int)
@click.option('--port', '-p', 'port', type=int, default=12345, help='port number')
@click.option('--debug', '-d', 'debug', is_flag=True, default=False,
              help='debug flag')
@click.pass_obj
def dc_mtr_server(obj, pin1, pin2, pin3, pin4, port, debug):
    """ dc_mtr_server """
    __log = get_logger(__name__, obj['debug'] or debug)
    __log.debug('obj=%s, pin=%s, port=%s', obj,
                (pin1, pin2, pin3, pin4), port)

    pi = pigpio.pi()
    test_app = Test_DcMtrServer(
        pi, ((pin1, pin2), (pin3, pin4)), port, obj['debug'] or debug)

    try:
        __log.info("start")
        test_app.main()

    finally:
        __log.info("end")
        pi.stop()
