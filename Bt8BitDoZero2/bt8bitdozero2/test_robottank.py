#
# Copyright (c) 2023 Yoichi Tanibayashi
#
# -*- coding: utf-8 -*-
#
import click
import time
from cmdclientserver import CmdClient
from .my_logger import get_logger
from . import Bt8BitDoZero2, Bt8BitDoZero2N


class Test_RobotTank:
    """ Test Bt8BitDoZero2 class """

    SPEED_MAX = 100
    SPEED_STEP = 30
    DEF_BASES_SPEED = 60
    CALIB_STEP = 5
    ROT_STEP = 30
    DELAY1 = 0.05
    DELAY_TURN = 0.4

    def __init__(self, devs, dc_mtr, debug=False):
        self._dbg = debug
        __class__.__log = get_logger(__class__.__name__, self._dbg)
        self.__log.debug('devs=%s', devs)

        self._devs = devs
        self._dc_mtr = dc_mtr

        self._bt8bitdozero2 = Bt8BitDoZero2N(
            self._devs, self.cb_func, debug=self._dbg)

        self._speed = [0, 0]
        self._base_speed = [self.DEF_BASES_SPEED, self.DEF_BASES_SPEED]
        self._prev_code = None
        self._prev_val = None

    def main(self):
        self.__log.debug('')

        self._bt8bitdozero2.start()

        while True:
            self.__log.debug(time.strftime('%Y/%m/%d(%a) %H:%M:%S'))
            time.sleep(5)

    def speed_add1(self, a, b):
        ret = int(a) + int(b)
        if b > 0 and ret > self.SPEED_MAX:
            ret = self.SPEED_MAX
        if b < 0 and ret < -self.SPEED_MAX:
            ret = -self.SPEED_MAX

        return ret

    def speed_add(self, step):
        self._speed[0] = self.speed_add1(self._speed[0], step[0])
        self._speed[1] = self.speed_add1(self._speed[1], step[1])

    def cb_func(self, dev, evtype, code, val):
        """ callback function """
        self.__log.debug('')

        # !! code_strがlistのこともある !!
        code_str = Bt8BitDoZero2.keycode2str(evtype, code)
        val_str = Bt8BitDoZero2.keyval2str(evtype, val)

        self.__log.info('dev=%d, evtype=%d, code=%d:%s, val=%d:%s',
                        dev, evtype, code, code_str, val, val_str)

        if val_str in ['MIDDLE']:
            return

        d_speed = [0, 0]

        if val_str in ['RELEASE']:
            self._speed = [0, 0]

        if [evtype, code] == Bt8BitDoZero2.BTN['A'] and val_str == 'PUSH':
            self._speed = [self._base_speed[0], self._base_speed[1]]

        if [evtype, code] == Bt8BitDoZero2.BTN['Y'] and val_str == 'PUSH':
            self._speed = [-self._base_speed[0], -self._base_speed[1]]

        if [evtype, code] == Bt8BitDoZero2.BTN['X'] and val_str == 'PUSH':
            self._speed = [-self._base_speed[0], self._base_speed[1]]

        if [evtype, code] == Bt8BitDoZero2.BTN['B'] and val_str == 'PUSH':
            self._speed = [self._base_speed[0], -self._base_speed[1]]

        # calibration
        if [evtype, code] == Bt8BitDoZero2.BTN['UD'] and val_str == 'LOW':
            self._base_speed[0] = self.speed_add1(self._base_speed[0],
                                                  -self.CALIB_STEP)
            self._base_speed[1] = self.speed_add1(self._base_speed[0],
                                                  +self.CALIB_STEP)

            d_speed = [-self.CALIB_STEP, self.CALIB_STEP]

        if [evtype, code] == Bt8BitDoZero2.BTN['UD'] and val_str == 'HIGH':
            self._base_speed[0] = self.speed_add1(self._base_speed[0],
                                                  +self.CALIB_STEP)
            self._base_speed[1] = self.speed_add1(self._base_speed[0],
                                                  -self.CALIB_STEP)

            d_speed = [self.CALIB_STEP, -self.CALIB_STEP]

        if [evtype, code] == Bt8BitDoZero2.BTN['LR'] and val_str == 'HIGH':

            self._base_speed[0] = self.speed_add1(self._base_speed[0],
                                                  +self.CALIB_STEP)
            self._base_speed[1] = self.speed_add1(self._base_speed[0],
                                                  +self.CALIB_STEP)

            d_speed = [self.CALIB_STEP, self.CALIB_STEP]

        if [evtype, code] == Bt8BitDoZero2.BTN['LR'] and val_str == 'LOW':
            self._base_speed[0] = self.speed_add1(self._base_speed[0],
                                                  -self.CALIB_STEP)
            self._base_speed[1] = self.speed_add1(self._base_speed[0],
                                                  -self.CALIB_STEP)

            d_speed = [-self.CALIB_STEP, -self.CALIB_STEP]

        # move
        self.speed_add(d_speed)
        #self._dc_mtr.send_cmdline('speed %s %s' % tuple(self._speed))
        ret = self._dc_mtr.call('SPEED %s %s' % tuple(self._speed))
        self.__log.debug('ret=%s', ret)

        self._prev_code = code
        self._prev_val = val


@click.command(help="Robot Tank")
@click.argument('devs', metavar='dev_num[0|1|2|4..]...', type=int, nargs=-1)
@click.option('--svr_host', '-s', 'svr_host', type=str, default='localhost',
              help='server hostname')
@click.option('--svr_port', '-p', 'svr_port', type=int, default=12345,
              help='server port number')
@click.option('--debug', '-d', 'debug', is_flag=True, default=False,
              help='debug flag')
@click.pass_obj
def robottank(obj, devs, svr_host, svr_port, debug):
    """ ab_shutter """
    __log = get_logger(__name__, obj['debug'] or debug)
    __log.debug('obj=%s, devs=%s', obj, devs)

    dc_mtr = CmdClient(svr_host, svr_port, obj['debug'] or debug)
    test_app = Test_RobotTank(devs, dc_mtr, obj['debug'] or debug)

    try:
        test_app.main()

    finally:
        ret = dc_mtr.call('STOP')
        self.__log.debug('ret=%s', ret)
        print('END')
