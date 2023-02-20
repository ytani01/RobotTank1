#
# Copyright (c) 2023 Yoichi Tanibayahshi
#
# -*- coding: utf-8 -*-
#
import sys
import socketserver
from .my_logger import get_logger


class CmdHandler(socketserver.StreamRequestHandler):
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

    def net_recv(self):
        """
        Returns
        -------
        decoded_str: str
        """
        # recieve data
        try:
            data = self.rfile.readline().strip()
        except ConnectionResetError as e:
            self.__log.warning('%s:%s', type(e), e)
            return ''
        except BaseException as e:
            self.__log.warning('BaseException:%s:%s.', type(e), e)
            # XXX send stop
            return ''

        self.__log.debug('data=%a', data)

        # decode UTF-8
        try:
            decoded_str = data.decode('utf-8')
        except UnicodeDecodeError as e:
            self.__log.warning('%s:%s .. ignored', type(e).__name__, e)
            return ''
        else:
            self.__log.debug('decoded_str:%a', decoded_str)

        return decoded_str

    def net_send(self, msg):
        self.__log.debug('msg=%s.', msg)

        data = (msg + '\n').encode('utf-8')
        try:
            self.wfile.write(data)
        except BrokenPipeError as e:
            self.__log.debug('%s:%s', type(e).__name__, e)
        except Exception as e:
            self.__log.warning('%s:%s', type(e).__name__, e)

    def handle(self):
        # recv_data
        decoded_str = self.net_recv()

        # split: "A B C" --> ['A', 'B', 'C']
        args = decoded_str.split()
        if len(args) > 0:
            self.__log.debug('args=%s', args)
        else:
            self.net_send('NG NO_CMD')
            return

        # check cmd
        if args[0] not in self._svr._cmd:
            self.net_send('NG INVALID_CMD')
            return

        # exec cmd
        reply_str = self._svr._cmd[args[0]](args)
        self.__log.debug('reply_str=%s', reply_str)

        # send reply
        self.net_send(reply_str)

        # self.__log.info('%s %s', args, reply_str)


class CmdServer(socketserver.ThreadingTCPServer):
    """ TCP server """

    DEF_PORT = 54321

    def __init__(self, port=DEF_PORT, debug=False):
        """
        Parameters
        ----------
        port: int
        """
        self._dbg = debug
        __class__.__log = get_logger(__class__.__name__, self._dbg)
        self.__log.debug('port=%s', port)

        self._port = port

        self._cmd = {}
        self.add_cmd('HELLO', self.cmd_hello)

        try:
            super().__init__(('', self._port), CmdHandler)
        except Exception as e:
            self.__log.error('%s:%s', type(e).__name__, e)
            sys.exit(1)

    def add_cmd(self, cmd_name, func):
        """
        Parameters
        ----------
        cmd_name: str
        func: lambda list(str)
        """
        self._cmd[cmd_name] = func
        self.__log.debug('cmd={%a: %s}', cmd_name, func.__name__)

    def cmd_hello(self, args):
        """
        sample cmd function

        Parameters
        ----------
        args: list(str)
        """
        self.__log.debug('args=%s', args)
        return 'OK HELLO'
