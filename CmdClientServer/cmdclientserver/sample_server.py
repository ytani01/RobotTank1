#
# Copyright (c) 2023 Yoichi Tanibayahshi
#
# -*- coding: utf-8 -*-
#
import click
import datetime
from .my_logger import get_logger
from . import CmdServer


class CmdServerApp:
    def __init__(self, port, debug=False):
        self._dbg = debug
        __class__.__log = get_logger(__class__.__name__, self._dbg)
        self.__log.debug('port=%s', port)

        self._svr = CmdServer(port, debug=self._dbg)

        self._svr.add_cmd('ECHO', self.cmd_echo)
        self._svr.add_cmd('NOW', self.cmd_now)

    def main(self):
        try:
            self._svr.serve_forever()
        except KeyboardInterrupt as e:
            self.__log.error('%s:%s', type(e).__name__, e)
        except Exception as e:
            self.__log.error('%s:%s', type(e).__name__, e)

    def cmd_echo(self, args):
        self.__log.debug('args=%s', args)
        return 'OK ' + ' '.join(args[1:])

    def cmd_now(self, args):
        self.__log.debug('args=%s', args)
        if len(args) != 1:
            return 'NG'

        str = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
        return 'OK ' + str


@click.command(help="Sample Cmd Server")
@click.option('--port', '-p', 'port', type=int, default=54321,
              help='port number')
@click.option('--debug', '-d', 'debug', is_flag=True, default=False,
              help='debug option')
@click.pass_obj
def cmdserver(obj, port, debug):
    __log = get_logger(__name__, obj['debug'] or debug)
    __log.debug('obj=%s', obj)
    __log.debug('port=%s', port)

    app = CmdServerApp(port, obj['debug'] or debug)
    try:
        __log.info('START')
        app.main()
    finally:
        __log.info('END')
