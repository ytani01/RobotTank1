#!/usr/bin/env python3
#
# Copyright (c) 2023 Yoichi Tanibayashi
#
# -*- coding: utf-8 -*-
#
import click
from .my_logger import get_logger
from . import Vl53l0xServer


class Test_Vl53l0xServer:
    """
    """
    def __init__(self, offset, i2c_bus, i2c_addr, port, debug=False):
        """
        Parameters
        ----------
        offset: float
        i2c_bus: int
        i2c_addr: int
        port: int
        """
        self._dbg = debug
        __class__.__log = get_logger(__class__.__name__, self._dbg)
        self.__log.debug('offset=%s, i2c_bus:%s, i2c_addr=0x%02X, port=%s',
                         offset, i2c_bus, i2c_addr, port)

        self._offset = offset
        self._i2c_bus = i2c_bus
        self._i2c_addr = i2c_addr
        self._port = port

        self._svr = Vl53l0xServer(
            self._offset, self._i2c_bus, self._i2c_addr, self._port,
            debug=self._dbg)

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


@click.command(help="VL53L0X server")
@click.option('--offset', '-o', 'offset', type=float, default=0.0,
              help='distance offset')
@click.option('--i2cbus', '-b', 'i2cbus', type=int, default=1,
              help='I2C bus')
@click.option('--i2caddr', '-a', 'i2caddr', type=int, default=0x29,
              help='I2C address')
@click.option('--port', '-p', 'port', type=int, default=12346,
              help='port number')
@click.option('--debug', '-d', 'debug', is_flag=True, default=False,
              help='debug flag')
@click.pass_obj
def server(obj, offset, i2cbus, i2caddr, port, debug):
    """ vl53l0x_server """
    __log = get_logger(__name__, obj['debug'] or debug)
    __log.debug('obj=%s', obj)
    __log.debug('offset=%s, i2cbus=%s, i2caddr=0x%02X, port=%s',
                offset, i2cbus, i2caddr, port)

    test_app = Test_Vl53l0xServer(
        offset, i2cbus, i2caddr, port, obj['debug'] or debug)

    __log.info("START")
    try:
        test_app.main()

    finally:
        __log.info("END")
