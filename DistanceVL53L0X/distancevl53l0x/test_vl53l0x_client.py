#!/usr/bin/env python3
#
# Copyright (c) 2023 Yoichi Tanibayashi
#
# -*- coding: utf-8 -*-
#
import click
import cuilib
from .my_logger import get_logger
from . import Vl53l0xClient


class Test_Vl53l0xClient:
    """ Test_Vl53l0xClient """

    DEF_SPEED = 60
    D_SPEED = 5
    STOP_DELAY = 0.1
    BREAK_DELAY = 0.5

    def __init__(self, svr_host, svr_port, cmdline='', debug=False):
        self._dbg = debug
        __class__.__log = get_logger(__class__.__name__, self._dbg)
        self.__log.debug('svr: %s:%s', svr_host, svr_port)

        self._svr_host = svr_host
        self._svr_port = svr_port
        self._cmdline = cmdline

        self._clnt = Vl53l0xClient(
            self._svr_host, self._svr_port, debug=self._dbg)

        self.speed = [0, 0]

        self.cui = cuilib.Cui()
        self.cui.add('hH?', self.cui.help, 'Help')
        self.cui.add(['q', 'Q', 'KEY_ESCAPE'], self.cmd_quit, 'Quit')

        self.cui.add('gG', self.cmd_get_distance, 'Get Distance')

    def main(self):
        self.__log.debug('')

        if len(self._cmdline) > 0:
            self.send_cmdline(self._cmdline)
            return

        self.cui.start()
        self.cui.join()

    def send_cmdline(self, cmdline):
        """
        Parameters
        ----------
        cmdline: str

        Returns
        -------
        ret_str: str
        """

        ret_str = ''
        try:
            ret_str = self._clnt.send_cmdline(cmdline)
        except Exception as e:
            self.__log.error('%s:%s', type(e).__name__, e)

        return ret_str

    def cmd_quit(self, key_sym):
        self.__log.info('')
        self.cui.end()

    def cmd_get_distance(self, key_sym):
        self.__log.debug('key_sym=%s', key_sym)
        cmdline = 'get_distance'
        ret_str = self.send_cmdline(cmdline)
        self.__log.info('ret_str=%a', ret_str)


@click.command(help="dc_mtr_client")
@click.argument('cmdline', type=str, nargs=-1)
@click.option('--svr_host', '-s', 'svr_host', type=str, default='localhost',
              help='server hostname')
@click.option('--svr_port', '-p', 'svr_port', type=int, default=12346,
              help='server port number')
@click.option('--debug', '-d', 'debug', is_flag=True, default=False,
              help='debug flag')
@click.pass_obj
def client(obj, cmdline, svr_host, svr_port, debug):
    """ dc_mtr_client """
    __log = get_logger(__name__, obj['debug'] or debug)
    __log.debug('obj=%s, cmdline=%s, svr_host=%s, svr_port=%s',
                obj, cmdline, svr_host, svr_port)

    test_app = Test_Vl53l0xClient(
        svr_host, svr_port, ' '.join(cmdline), obj['debug'] or debug)

    try:
        test_app.main()

    finally:
        __log.info('end')
