#
# Copyright (c) 2023 Yoichi Tanibayahshi
#
# -*- coding: utf-8 -*-
#
import socketserver
import threading
import time
from .my_logger import get_logger
from .VL53L0X import VL53L0X, Vl53l0xAccuracyMode


CMD = {
    'GET_DISTANCE': ['get_distance', 'distance', 'get'],
    'GET_OFFSET': ['get_offset', 'offset'],
    'SET_OFFSET': ['set_offset'],
    'NULL': ['null']
}


class Vl53l0xWorker(threading.Thread):
    """ worker thread """

    def __init__(self, sensor, svr, debug=False):
        """
        Parameters
        ----------
        sensor: VL53L0X
        svr: Vl53l0xServer
        """
        self._dbg = debug
        __class__.__log = get_logger(__class__.__name__, self._dbg)
        self.__log.debug('')

        self._sensor = sensor
        self._svr = svr

        self.active = False

        super().__init__(daemon=True)

    def end(self):
        self.__log.debug('')

        self.active = False
        self.join()

        self._log.debug('END')

    def run(self):
        self.__log.debug('START')

        interval = self._sensor.get_timing()
        self.__log.debug('interval=%s', interval)

        self.active = True

        while self.active:
            try:
                self._svr._distance = self._sensor.get_distance()
                self._svr._distance += self._svr._offset
                self.__log.debug('distance=%s', self._svr._distance)
            except Exception as e:
                # XXX
                self.__log.warning('%s:%s', type(e).__name__, e)

            time.sleep(interval / 1000000.0)

        self.__log.info('END')


class Vl53l0xHandler(socketserver.StreamRequestHandler):
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

        data = msg.encode('utf-8')

        try:
            self.wfile.write(data)
        except BrokenPipeError as e:
            self.__log.debug('%s:%s', type(e).__name__, e)
        except Exception as e:
            self.__log.warning('%s:%s', type(e).__name__, e)

    def handle(self):
        net_data = b''

        while True:
            # receive data
            try:
                net_data = self._req.recv(512)
            except ConnectionResetError as e:
                self.__log.warning('%s:%s', type(e), e)
                return
            except BaseException as e:
                self.__log.warning('BaseException:%s:%s.', type(e), e)
                # XXX send stop
                return

            if len(net_data) == 0:
                # disconnect
                break

            # decode UTF-8
            try:
                decoded_data = net_data.decode('utf-8')
            except UnicodeDecodeError as e:
                self.__log.warning('%s:%s .. ignored', type(e).__name__, e)
                continue
            else:
                self.__log.debug('decoded_data:%a', decoded_data)

            # split: "A B C" --> ['A', 'B', 'C']
            cmd = decoded_data.split()
            if len(cmd) > 0:
                self.__log.info('cmd=%s', cmd)

            # execute cmd
            if cmd[0] in CMD['GET_DISTANCE']:
                msg = 'OK %s' % (self._svr._distance)
                self.net_write(msg)
                break

            # invalid cmd
            self.net_write('NG')

        self.__log.debug('END')


class Vl53l0xServer(socketserver.ThreadingTCPServer):
    """ TCP server """

    DEF_PORT = 12346

    def __init__(self, offset=0.0, i2c_bus=1, i2c_addr=0x29, port=DEF_PORT,
                 debug=False):
        """
        Parameters
        ----------
        offset: float
        i2c_bus: int
        i2c_addr: int
        port: int
        """
        self._dbg = debug
        __class__.__log = get_logger(__class__.__name__, self._dbg)
        self.__log.debug('offset=%s, i2c_bus=%s, i2c_addr=0x%02X, port=%s',
                         offset, i2c_bus, i2c_addr, port)

        self._offset = offset
        self._i2c_bus = i2c_bus
        self._i2c_addr = i2c_addr
        self._port = port

        self._distance = 0.0

        self._sensor = VL53L0X(self._i2c_bus, self._i2c_addr)
        self._sensor.open()
        self._sensor.start_ranging(Vl53l0xAccuracyMode.LONG_RANGE)

        self._sensor_worker = Vl53l0xWorker(self._sensor, self, self._dbg)
        self._sensor_worker.start()

        try:
            super().__init__(('', self._port), Vl53l0xHandler)
        except Exception as e:
            self.__log.warning('%s:%s', type(e).__name__, e)
            return None
