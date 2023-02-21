#!/usr/bin/env python3
#
# Copyright (c) 2023 Yoichi Tanibayashi
#
# -*- coding: utf-8 -*-
#
import pigpio
import threading
import queue
import time
import click
from cmdclientserver import CmdServer
from . import DcMtrN
from .my_logger import get_logger


class Worker(threading.Thread):
    """ worker thread """

    def __init__(self, mtr, svr, debug=False):
        self._dbg = debug
        __class__.__log = get_logger(__class__.__name__, self._dbg)
        self.__log.debug('')

        self._mtr = mtr
        self._svr = svr

        self._active = False
        self._cmdq = queue.SimpleQueue()  # list(str)

        super().__init__(daemon=True)

    def end(self):
        self.__log.debug('')

        self._active = False
        self.join()

        self.__log.debug('done')

    def send(self, cmd):
        """
        Parameters
        ----------
        cmd: list(str)
        """
        self.__log.debug('cmd=%s', cmd)

        self._cmdq.put(cmd)

    def recv(self):
        """
        Returns
        -------
        cmd: list(str)
        """
        self.__log.debug('...')

        cmd = self._cmdq.get()
        self.__log.debug('cmd=%s', cmd)

        return cmd

    def clear_cmds(self):
        self.__log.debug('')

        while not self._cmdq.empty():
            try:
                cmd = self._cmdq.get_nowait()
            except queue.Empty as e:
                self.__log.debug('%s:%s', type(e).__name__, e)
            except Exception as e:
                self.__log.error('%s:%s', type(e).__name__, e)
                break
            else:
                self.__log.info('ignore cmd: %s', cmd)

    def run(self):
        self.__log.debug('')

        self._active = True
        while self._active:
            cmd = self.recv()
            self.__log.debug('cmd=%s', cmd)

            if len(cmd) == 0:
                self.__log.error('cmd=%s !?', cmd)
                break

            try:
                if cmd[0] == 'SPEED':
                    if len(cmd) != 3:
                        self.__log.error('%s .. ignored', cmd)
                        continue

                    self._mtr.set_speed((int(cmd[1]), int(cmd[2])))
                    continue

                if cmd[0] == 'STOP':
                    self._mtr.set_stop()
                    continue

                if cmd[0] == 'BREAK':
                    self._mtr.set_break()
                    continue

                if cmd[0] == 'DELAY':
                    if len(cmd) != 2:
                        self.__log.err('%s .. ignored', cmd)
                        continue

                    self.__log.debug('delay %s sec', cmd[1])

                    time.sleep(float(cmd[1]))
                    continue

                if cmd[0] == 'NULL':
                    continue

                self.__log.error('Invalid cmd: %s', cmd)

            except KeyboardInterrupt as e:
                self._mtr.set_stop()
                self.__log.warning('%s:%s', type(e).__name__, e)

            except Exception as e:
                self._mtr.set_stop()
                self.__log.warning('%s:%s', type(e).__name__, e)

        self.__log.info('END')


class ServerApp:
    def __init__(self, pi, pin, port, debug=False):
        self._dbg = debug
        __class__.__log = get_logger(__class__.__name__, self._dbg)
        self.__log.debug('pin=%s, port=%s', pin, port)

        self._pi = pi
        self._pin = pin
        self._port = port

        self._mtr = DcMtrN(self._pi, self._pin, self._dbg)

        self._worker = Worker(self._mtr, self, self._dbg)
        self._worker.start()

        self._svr = CmdServer(self._port, debug=self._dbg)

        self._svr.add_cmd('SPEED', self.cmd_normal)
        self._svr.add_cmd('STOP', self.cmd_normal)
        self._svr.add_cmd('BREAK', self.cmd_normal)
        self._svr.add_cmd('DELAY', self.cmd_normal)
        self._svr.add_cmd('CLEAR', self.cmd_clear)

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

    def cmd_normal(self, args):
        """
        Parameters
        ----------
        args: list(str)

        Returns
        -------
        ret: str
        """
        self.__log.debug('args=%s', args)

        self._worker.send(args)

        return 'OK'

    def cmd_clear(self, args):
        """
        Parameters
        ----------
        args: list(str)

        Returns
        -------
        ret: str
        """
        self.__log.debug('args=%s', args)

        self._worker.clear_cmds()
        self._worker.send(['STOP'])

        return 'OK'


@click.command(help="DC Motor Server")
@click.argument('pin1', type=int)
@click.argument('pin2', type=int)
@click.argument('pin3', type=int)
@click.argument('pin4', type=int)
@click.option('--port', '-p', 'port', type=int, default=12345,
              help='port number')
@click.option('--debug', '-d', 'debug', is_flag=True, default=False,
              help='debug flag')
@click.pass_obj
def server(obj, pin1, pin2, pin3, pin4, port, debug):
    __log = get_logger(__name__, obj['debug'] or debug)
    __log.debug('obj=%s', obj)
    __log.debug('pin=%s, port=%s', (pin1, pin2, pin3, pin4), port)

    pi = pigpio.pi()
    pins = ((pin1, pin2), (pin3, pin4))

    app = ServerApp(pi, pins, port, obj['debug'] or debug)

    try:
        __log.info("START")
        app.main()

    finally:
        self._pi.stop()
        __log.info("END")
