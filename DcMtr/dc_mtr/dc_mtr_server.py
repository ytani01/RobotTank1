#!/usr/bin/env python3
#
# Copyright (c) 2023 Yoichi Tanibayahshi
#
# -*- coding: utf-8 -*-
#
import socketserver
from .my_logger import get_logger
from . import DcMtrN


class DcMtrHandler(socketserver.StreamRequestHandler):
    """ handler
    """

    CMD = {
        'speed': ['speed', 'v', 'V'],
        'stop': ['stop', 's', 'S'],
        'break': ['break', 'b', 'B'],
        'null': ['null']
    }

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
        self.__log.debug('msg=%a', msg)

        msg_data = msg.encode('utf-8')
        self.__log.debug('msg_data=%a', msg_data)

        try:
            self.wfile.write(msg_data)
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
            cmd = decoded_data.split()
            self.__log.info('cmd=%s', cmd)

            if len(cmd) == 0:
                msg = 'No data .. disconnect'
                self.__log.warning(msg)
                break

            # exec
            ret_msg = 'NG %s\n' % (cmd)
            if cmd[0] in self.CMD['speed']:
                if len(cmd) == 3:
                    self._svr._mtr.set_speed((int(cmd[1]), int(cmd[2])))
                    ret_msg = 'OK %s\n' % (cmd)
                else:
                    self.__log.warning("%s .. ignored", cmd)
                    ret_msg = 'NG %s\n' % (cmd)

            if cmd[0] in self.CMD['stop']:
                self._svr._mtr.set_stop()
                ret_msg = 'OK %s\n' % (cmd)

            if cmd[0] in self.CMD['break']:
                self._svr._mtr.set_break()
                ret_msg = 'OK %s\n' % (cmd)

            if cmd[0] in self.CMD['null']:
                ret_msg = 'OK %s\n' % (cmd)

            self.net_write(ret_msg)

        self.__log.info('done')

    def finish(self):
        self.__log.debug('')


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

        try:
            super().__init__(('', self._port), DcMtrHandler)
        except Exception as e:
            self.__log.warning('%s:%s', type(e).__name__, e)
            return None
