#
# Copyright (c) 2023 Yoichi Tanibayahshi
#
# -*- coding: utf-8 -*-
#
import click
from cmdclientserver import CmdServer
from .my_logger import get_logger
from . import DistanceVL53L0X


class CmdServerApp:
    def __init__(self, offset, port, debug=False):
        self._dbg = debug
        __class__.__log = get_logger(__class__.__name__, self._dbg)
        self.__log.debug('offset=%s, port=%s', offset, port)

        self._offset = offset
        self._port = port

        self._sensor = DistanceVL53L0X(self._offset, debug=self._dbg)

        self._svr = CmdServer(self._port, debug=self._dbg)

        self._svr.add_cmd('GET_DISTANCE', self.cmd_get_distance)

    def main(self):
        self._sensor.start()
        self._sensor.wait_active()

        try:
            self._svr.serve_forever()
        except KeyboardInterrupt as e:
            self.__log.error('%s:%s', type(e).__name__, e)
        except Exception as e:
            self.__log.error('%s:%s', type(e).__name__, e)

        self._sensor.end()

    def cmd_get_distance(self, args):
        self.__log.debug('args=%s', args)
        if len(args) != 1:
            return 'NG'

        distance = self._sensor.get_distance()
        self.__log.debug('distance=%s', distance)

        return 'OK %s' % (distance)


@click.command(help="Distance Server")
@click.option('--offset', '-o', 'offset', type=float, default=0.0,
              help='sensor offset')
@click.option('--port', '-p', 'port', type=int, default=12347,
              help='port number')
@click.option('--debug', '-d', 'debug', is_flag=True, default=False,
              help='debug option')
@click.pass_obj
def server(obj, offset, port, debug):
    __log = get_logger(__name__, obj['debug'] or debug)
    __log.debug('obj=%s', obj)
    __log.debug('offset=%s, port=%s', offset, port)

    app = CmdServerApp(offset, port, obj['debug'] or debug)
    try:
        __log.info('START')
        app.main()
    finally:
        __log.info('END')
