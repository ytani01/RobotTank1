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


class DcMtrWorker(threading.Thread):
    """ worker thread """

    def __init__(self, pi, mtr, debug=False):
        self._dbg = debug
        __class__.__log = get_logger(__class__.__name__, self._dbg)
        self.__log.debug('')

        self._mtr = mtr

        self.active =False
        self.cmdq = queue.Queue()

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
        self.__log.debug('')
        cmd = self.cmdq.get()
        self.__log.debug('cmd=%s', cmd)
        return cmd

    def run(self):
        self.__log.debug('')

        self.active = True
        while self.active:
            cmd = self.recv()
            self.__log.debug('cmd=%s', cmd)

            try:
                if cmd[0] == "speed":
                    self._mtr.set_speed((int(cmd[1]), int(cmd[2])))
                    continue

                if cmd[0] == "stop":
                    self._mtr.set_stop()
                    continue

                if cmd[0] == "break":
                    self._mtr.set_break()
                    continue

                if cmd[0] == "delay":
                    self.__log.info('delay: %s sec', cmd[1])
                    time.sleep(float(cmd[1]))
                    self.__log.info('delay: %s sec: done', cmd[1])
                    continue

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
        except BronkenPipeError as e:
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
                # XXX send stop
                return

            # decode UTF-8
            try:
                decoded_data = net_data.decode('utf-8')
            except UnicodeDecodeError as e:
                self.__log.warning('%s:%s .. ignored', type(e).__name__, e)
                continue
            else:
                self.__log.debug('decoded_data:%a', decoded_data)

            # remove white spaces and split
            data = decoded_data.split()
            self.__log.debug('data=%a', data)

            if len(data) == 0:
                msg = 'No data .. disconnect'
                self.__log.warning(msg)
                break

            self._svr._mtr_worker.send(data)

        self.__log.info('done')


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
        self._mtr_worker = DcMtrWorker(self._pi, self._mtr, self._dbg)
        self._mtr_worker.start()

        try:
            super().__init__(('', self._port), DcMtrHandler)
        except Exception as e:
            self.__log.warning('%s:%s', type(e).__name__, e)
            return None
