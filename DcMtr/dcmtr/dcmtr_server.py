#
# Copyright (c) 2023 Yoichi Tanibayashi
#
# -*- coding: utf-8 -*-
#
import sys
import pigpio
import threading
import queue
import time
import click
from cmdclientserver import CmdServer
from .dcmtr_n import DcMtrN
from .my_logger import get_logger


DEF_PORT = 12345


class ServerWorker(threading.Thread):
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
        self.__log.debug('working ..')

        self._active = False
        self.join()

        self.__log.debug('END')

    def send(self, cmd):
        """
        Parameters
        ----------
        cmd: list(str)
        """
        self.__log.debug('cmd=%s', cmd)

        self._cmdq.put(cmd)

    def recv(self, timeout=2.0):
        """
        Returns
        -------
        cmd: list(str)
        """
        self.__log.debug('...')

        try:
            cmd = self._cmdq.get(timeout=timeout)
            self.__log.debug('cmd=%s', cmd)

        except Exception as e:
            self.__log.debug('%s:%s', type(e).__name__, e)
            cmd = []

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
                self.__log.debug('cmd is empty !?')
                continue

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

            except Exception as e:
                self._mtr.set_stop()
                self.__log.warning('%s:%s', type(e).__name__, e)

        self.__log.info('END: active=%s', self._active)


class ServerApp:
    def __init__(self, pi, pin, port=DEF_PORT, debug=False):
        self._dbg = debug
        __class__.__log = get_logger(__class__.__name__, self._dbg)
        self.__log.debug('pin=%s, port=%s', pin, port)

        self._pi = pi
        self._pin = pin
        self._port = port

        self._mtr = DcMtrN(self._pi, self._pin, debug=self._dbg)
        self._worker = ServerWorker(self._mtr, self, self._dbg)
        self._svr = CmdServer(self._port, debug=self._dbg)

        self._svr.add_cmd('SPEED', self.cmd_std)
        self._svr.add_cmd('STOP', self.cmd_std)
        self._svr.add_cmd('BREAK', self.cmd_std)
        self._svr.add_cmd('DELAY', self.cmd_std)
        self._svr.add_cmd('CLEAR', self.cmd_clear)

    def main(self):
        self.__log.info('start server')

        self._worker.start()

        try:
            self._svr.serve_forever()
        except ValueError as e:
            self.__log.error('%s:%s', type(e).__name__, e)
            self.__log.error('  port=%s: is in use (?)', self._port)

        except Exception as e:
            self.__log.error('%s:%s', type(e).__name__, e)

        except KeyboardInterrupt as e:
            self.__log.info('%s:%s', type(e).__name__, e)

        self._worker.end()
        self.__log.info('END')

    def cmd_std(self, args):
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
@click.argument('pin1_1', type=int, metavar='PIN1_1')
@click.argument('pin1_2', type=int, metavar='PIN1_2')
@click.argument('pin2_1', type=int, metavar='PIN2_1')
@click.argument('pin2_2', type=int, metavar='PIN2_2')
@click.option('--port', '-p', 'port', type=int, default=DEF_PORT,
              help='port number (default=%s)' % (DEF_PORT))
@click.option('--debug', '-d', 'debug', is_flag=True, default=False,
              help='debug flag')
@click.pass_obj
def server(obj, pin1_1, pin1_2, pin2_1, pin2_2, port, debug):
    __log = get_logger(__name__, obj['debug'] or debug)
    pins = ((pin1_1, pin1_2), (pin2_1, pin2_2))
    __log.debug('pins=%s, port=%s', pins, port)

    pi = pigpio.pi()
    res = 0
    app = ServerApp(pi, pins, port, obj['debug'] or debug)

    try:
        __log.info("START")
        app.main()

    except KeyboardInterrupt as e:
        __log.info('%s', type(e).__name__)

    except Exception as e:
        __log.error('%s:%s', type(e).__name__, e)
        res = 1

    finally:
        pi.stop()
        __log.info("END: res=%s", res)
        sys.exit(res)
