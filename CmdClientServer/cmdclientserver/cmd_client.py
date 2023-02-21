#
# Copyright (c) 2023 Yoichi Tanibayahshi
#
# -*- coding: utf-8 -*-
#
import socket
from .my_logger import get_logger


class CmdClient:
    """ CmdClient
    """
    DEF_HOST = 'localhost'
    DEF_PORT = 54321

    BUFSIZE = 512

    def __init__(self, svr_host=DEF_HOST, svr_port=DEF_PORT, debug=False):
        """ init """
        self._dbg = debug
        __class__.__log = get_logger(__class__.__name__, self._dbg)
        self.__log.debug('svr: %s:%s', svr_host, svr_port)

        self._svr_host = svr_host
        self._svr_port = svr_port

    def call(self, cmdline):
        self.__log.debug('cmdline=%a', cmdline)

        rep_str = ''
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                # send
                sock.connect((self._svr_host, self._svr_port))
                sock.sendall(bytes(cmdline + '\n', 'utf-8'))

                # receive
                rep_str = str(sock.recv(self.BUFSIZE), 'utf-8').strip()
                self.__log.debug('rep_str=%a', rep_str)

                return rep_str

        except Exception as e:
            msg = '%s:%s' % (type(e).__name__, e)
            self.__log.error(msg)
            rep_str = 'NG ' + msg

        return rep_str
