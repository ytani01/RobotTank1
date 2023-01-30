#!/usr/bin/env python3
#
# Copyright (c) 2023 Yoichi Tanibayashi
#
# -*- coding: utf-8 -*-
#
import click
import sys
import cuilib
from .my_logger import get_logger
from . import DcMtrClient


class Test_DcMtrClient:
    """ Test_DcMtrClient """

    DEF_SPEED = 60

    def __init__(self, svr_host, svr_port, cmdline='', debug=False):
        self._dbg = debug
        __class__.__log = get_logger(__class__.__name__, self._dbg)
        self.__log.debug('svr: %s:%s', svr_host, svr_port)

        self._svr_host = svr_host
        self._svr_port = svr_port
        self._cmdline = cmdline

        self._clnt = DcMtrClient(
            self._svr_host, self._svr_port, debug=self._dbg)

        self.speed = [0, 0]

        self.cui = cuilib.Cui()
        self.cui.add('hH?', self.cui.help, 'Help')
        self.cui.add(['Q', 'KEY_ESCAPE'], self.cmd_quit, 'Quit')

        self.cui.add('sS', self.cmd_stop, 'Stop')
        self.cui.add(' ', self.cmd_break, 'Break')
        self.cui.add('w', self.cmd_forward, 'Forward')
        self.cui.add('x', self.cmd_backward, 'Backward')
        self.cui.add('a', self.cmd_left, 'Left')
        self.cui.add('d', self.cmd_right, 'Right')

    def main(self):
        self.__log.debug('')

        if len(self._cmdline) > 0:
            self._clnt.send_cmdline(self._cmdline)
            return

        self.cui.start()
        self.cui.join()

    def set_speed(self, speed):
        self.__log.debug('speed=%s', speed)
        self.speed = speed
        cmdline = 'speed %s %s' % tuple(self.speed)
        self.__log.debug('cmdline=%s', cmdline)
        self._clnt.send_cmdline(cmdline)

    def cmd_quit(self, key_sym):
        self.__log.info('')
        self.cmd_break(key_sym)
        self.cui.end()

    def cmd_forward(self, key_sym):
        self.set_speed([self.DEF_SPEED, self.DEF_SPEED])

    def cmd_backward(self, key_sym):
        self.set_speed([-self.DEF_SPEED, -self.DEF_SPEED])

    def cmd_left(self, key_sym):
        self.set_speed([-self.DEF_SPEED, self.DEF_SPEED])

    def cmd_right(self, key_sym):
        self.set_speed([self.DEF_SPEED, -self.DEF_SPEED])

    def cmd_stop(self, key_sym):
        self.set_speed([0, 0])

    def cmd_break(self, key_sym):
        self.__log.debug('')
        self._clnt.send_cmdline('break')


@click.command(help="dc_mtr_client")
@click.argument('cmdline', type=str, nargs=-1)
@click.option('--svr_host', '-s', 'svr_host', type=str, default='localhost',
              help='server hostname')
@click.option('--svr_port', '-p', 'svr_port', type=int, default=12345,
              help='server port number')
@click.option('--debug', '-d', 'debug', is_flag=True, default=False,
              help='debug flag')
@click.pass_obj
def dc_mtr_client(obj, cmdline, svr_host, svr_port, debug):
    """ dc_mtr_client """
    __log = get_logger(__name__, obj['debug'] or debug)
    __log.debug('obj=%s, cmdline=%s, svr_host=%s, svr_port=%s',
                obj, cmdline, svr_host, svr_port)

    test_app = Test_DcMtrClient(
        svr_host, svr_port, ' '.join(cmdline), obj['debug'] or debug)

    try:
        test_app.main()

    finally:
        __log.info('end')
