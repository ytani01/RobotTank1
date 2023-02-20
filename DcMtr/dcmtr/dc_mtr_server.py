#!/usr/bin/env python3
#
# Copyright (c) 2023 Yoichi Tanibayahshi
#
# -*- coding: utf-8 -*-
#
import socketserver
import threading
import queue
import time
from .my_logger import get_logger
from . import DcMtrN


CMD = {
    'SPEED': ['speed', 'v', 'V'],
    'STOP': ['stop', 's', 'S'],
    'BREAK': ['break', 'b', 'B' ' '],
    'DELAY': ['delay', 'sleep', 't', 'T'],
    'CLEAR': ['clear', 'cancel', 'c', 'C'],
    'NULL': ['null']
}


class DcMtrWorker(threading.Thread):
    """ worker thread """

    def __init__(self, pi, mtr, svr, debug=False):
        self._dbg = debug
        __class__.__log = get_logger(__class__.__name__, self._dbg)
        self.__log.debug('')

        self._mtr = mtr
        self._svr = svr

        self.active = False
        self.cmdq = queue.SimpleQueue()

        super().__init__(daemon=True)

    def end(self):
        self.__log.debug('')

        self.join()

        self._log.debug('done')

    def send(self, cmd, doInterrupt=True):
        """
        cmd: "<cmd_name> <params>.."
        """
        self.__log.debug('cmd=%s', cmd)

        self.cmdq.put(cmd)

    def recv(self):
        """
        """
        self.__log.debug('')

        cmd = self.cmdq.get()
        self.__log.debug('cmd=%s', cmd)

        return cmd

    def clear_cmds(self):
        """
        clear command queue
        """
        self.__log.debug('')

        while not self.cmdq.empty():
            try:
                cmd = self.cmdq.get_nowait()
            except queue.Empty as e:
                self.__log.debug('%s:%s', type(e).__name__, e)
                break
            except Exception as e:
                self.__log.error('%s:%s', type(e).__name__, e)
                break
            else:
                self.__log.debug('ignore cmd: %s', cmd)

    def run(self):
        self.__log.debug('')

        self.active = True
        while self.active:
            cmd = self.recv()
            self.__log.debug('cmd=%s', cmd)

            if len(cmd) == 0:
                break

            try:
                if cmd[0] in CMD['SPEED']:
                    if len(cmd) != 3:
                        self.__log.warning("%s .. ignored", cmd)
                        continue

                    self._mtr.set_speed((int(cmd[1]), int(cmd[2])))
                    continue

                if cmd[0] in CMD['STOP']:
                    self._mtr.set_stop()
                    continue

                if cmd[0] in CMD['BREAK']:
                    self._mtr.set_break()
                    continue

                if cmd[0] in CMD['DELAY']:
                    # XXX to be update
                    if len(cmd) != 2:
                        self.__log.warning("%s .. ignore", cmd)
                        continue

                    self.__log.debug('delay: %s sec', cmd[1])
                    time.sleep(float(cmd[1]))
                    continue

                if cmd[0] in CMD['NULL']:
                    continue

                self.__log.warning('Invalid cmd: %s', cmd)

            except Exception as e:
                self._mtr.set_stop()
                self.__log.warning('%s:%s', type(e).__name__, e)

        self.__log.info('done.')


class DcMtrHandler(socketserver.StreamRequestHandler):
    """ handler """
    def __init__(self, req, client_addr, svr):
        """ __init__ """
        self._dbg = svr._dbg
        __class__.__log = get_logger(__class__.__name__, self._dbg)
        self.__log.debug('client_addr: %s', client_addr)

        self._req = req
        self._client_addr = client_addr
        self._svr = svr

        super().__init__(self._req, self._client_addr, self._svr)

    def setup(self):
        self.__log.debug('')
        return super().setup()

    def net_write(self, msg):
        self.__log.debug('msg=%s.', msg)

        try:
            self.wfile.write(msg)
        except BrokenPipeError as e:
            self.__log.debug('%s:%s', type(e).__name__, e)
        except Exception as e:
            self.__log.warning('%s:%s', type(e).__name__, e)

    def handle(self):
        """ handle """
        self.__log.debug('')

        net_data = b''
        flag_continue = True
        while flag_continue:
            try:
                net_data = self._req.recv(512)
            except ConnectionResetError as e:
                self.__log.warning('%s:%s', type(e), e)
                return
            except BaseException as e:
                self.__log.warning('BaseException:%s:%s.', type(e), e)
                ## XXX send stop
                return

            ## decode UTF-8
            try:
                decoded_data = net_data.decode('utf-8')
            except UnicodeDecodeError as e:
                self.__log.warning('%s:%s .. ignored', type(e).__name__, e)
                continue
            else:
                self.__log.debug('decoded_data:%a', decoded_data)

            ## white spaces and split
            cmd = decoded_data.split()
            if len(cmd) > 0:
                self.__log.info('cmd=%s', cmd)

            if len(cmd) == 0:
                ## msg = 'No data .. disconnect'
                ## self.__log.warning(msg)
                break

            if cmd[0] in CMD['CLEAR']:
                self._svr._mtr_worker.clear_cmds()
                self._svr._mtr_worker.send([CMD['STOP'][0]])
                break

            self._svr._mtr_worker.send(cmd)

        self.__log.debug('done')


class DcMtrServer(socketserver.ThreadingTCPServer):
    """ TCP server """

    DEF_PORT = 12345

    def __init__(self, pi, pin, port=DEF_PORT, debug=False):
        """ __init__ """
        self._dbg = debug
        __class__.__log = get_logger(__class__.__name__, self._dbg)
        self.__log.debug('pin=%s, port=%s', pin, port)

        self._pi = pi
        self._pin = pin
        self._port = port

        self._mtr = DcMtrN(self._pi, self._pin, self._dbg)

        self._mtr_worker = DcMtrWorker(self._pi, self._mtr, self, self._dbg)
        self._mtr_worker.start()

        try:
            super().__init__(('', self._port), DcMtrHandler)
        except Exception as e:
            self.__log.warning('%s:%s', type(e).__name__, e)
            return None
