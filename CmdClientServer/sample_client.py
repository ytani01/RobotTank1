#!/usr/bin/env python3
#
# Copyright (c) 2023 Yoichi Tanibayahshi
#
# -*- coding: utf-8 -*-
#
import click
from cmdclientserver import CmdClient, get_logger


class CmdClientApp:
    def __init__(self, cmdline, svr_host, svr_port, debug=False):
        self._dbg = debug
        __class__.__log = get_logger(__class__.__name__, self._dbg)
        self.__log.debug('cmdline=%s', cmdline)
        self.__log.debug('svr=%s:%s', svr_host, svr_port)

        self._cmdline = cmdline
        self._clnt = CmdClient(svr_host, svr_port, self._dbg)

    def main(self):
        # 1st time
        cmdline = 'HELLO'
        rep_str = self._clnt.call(cmdline)
        self.__log.info('%a>%a', cmdline, rep_str)

        if not rep_str.startswith('OK'):
            return

        # 2nd time
        rep_str = self._clnt.call(self._cmdline)
        self.__log.info('%a>%a', self._cmdline, rep_str)


@click.command(context_settings=dict(help_option_names=['-h', '--help']),
               help='Cmd Client')
@click.argument('cmdline', metavar='cmdline ..', type=str, nargs=-1)
@click.option('--svr_host', '--host', '-s', 'svr_host',
              type=str, default='localhost',
              help='server host name')
@click.option('--svr_port', '--port', '-p', 'svr_port',
              type=int, default=54321,
              help='server port number')
@click.option('--debug', '-d', 'debug', is_flag=True, default=False,
              help='')
def main(cmdline, svr_host, svr_port, debug):
    __log = get_logger(__name__, debug)
    __log.debug('cmdline=%s, svr_host=%s, svr_port=%s',
                cmdline, svr_host, svr_port)

    cmdline_str = ' '.join(cmdline)
    app = CmdClientApp(cmdline_str, svr_host, svr_port, debug)
    try:
        __log.info('START')
        app.main()
    finally:
        __log.info('END')


if __name__ == '__main__':
    main()
