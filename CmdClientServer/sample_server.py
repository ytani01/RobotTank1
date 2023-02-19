#!/usr/bin/env python3
#
# Copyright (c) 2023 Yoichi Tanibayahshi
#
# -*- coding: utf-8 -*-
#
import click
import datetime
from cmdclientserver import CmdServer, get_logger


class CmdServerApp:
    def __init__(self, port, debug=False):
        self._dbg = debug
        __class__.__log = get_logger(__class__.__name__, self._dbg)
        self.__log.debug('port=%s', port)

        self._svr = CmdServer(port, debug=self._dbg)
        if self._svr is None:
            return None

        self._svr.add_cmd('ECHO', self.cmd_echo)
        self._svr.add_cmd('DATETIME', self.cmd_datetime)

    def main(self):
        self.__log.info('START')

        try:
            self._svr.serve_forever()
        except KeyboardInterrupt as e:
            self.__log.error('%s:%s', type(e).__name__, e)
        except Exception as e:
            self.__log.error('%s:%s', type(e).__name__, e)

        self.__log.info('END')

    def cmd_echo(self, args):
        self.__log.debug('args=%s', args)
        return 'OK ' + ' '.join(args[1:])

    def cmd_datetime(self, args):
        self.__log.debug('args=%s', args)
        if len(args) != 1:
            return 'NG'

        str = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
        return 'OK ' + str


@click.command(context_settings=dict(help_option_names=['-h', '--help']),
               help='Cmd Server')
@click.option('--port', '-p', 'port', type=int, default=54321,
              help='port number')
@click.option('--debug', '-d', 'debug', is_flag=True, default=False,
              help='')
def main(port, debug):
    __log = get_logger(__name__, debug)
    __log.debug('port=%s', port)

    app = CmdServerApp(port, debug)
    try:
        __log.info('START')
        app.main()
    finally:
        __log.info('END')


if __name__ == '__main__':
    main()
