#
# Copyright (c) 2023 Yoichi Tanibayashi
#
# -*- coding: utf-8 -*-
#
import click
import time
from dcmtr import DcMtrClient
from .my_logger import get_logger
from . import BtKbd


class Test_RobotTank:
    """ Test BtKbd class """

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

        self._btkbd = []
        for d in self._devs:
            btkbd = None
            while btkbd is None:
                try:
                    btkbd = BtKbd(d, self.cb_func, debug=self._dbg)
                except Exception as e:
                    self.__log.error('%s:%s', type(e).__name__, e)
                    time.sleep(2)
                else:
                    self.__log.info('connect: %s', d)

            self._btkbd.append(btkbd)

        self._speed = [0, 0]
        self._base_speed = [self.DEF_BASES_SPEED, self.DEF_BASES_SPEED]
        self._prev_keycode = None
        self._prev_keyval = None

    def main(self):
        self.__log.debug('')

        for btkbd in self._btkbd:
            btkbd.start()

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

    def cb_func(self, dev, code, value):
        """ callback function """

        keycode = BtKbd.keycode2str(code)
        if type(keycode) == list:  # !! keycodeがlistのこともある !!
            keycode = keycode[0]

        keyval = BtKbd.keyval2str(value)

        self.__log.info('dev=%d, code=%d:%s, value=%d:%s',
                        dev, code, keycode, value, keyval)


        if keyval in ['RELEASE', 'HOLD']:
            return

        # keyval in ['PUSH']

        d_speed = [0, 0]

        if keycode != self._prev_keycode:
            self._dc_mtr.send_cmdline('clear')
            self._dc_mtr.send_cmdline('delay %s' % (self.DELAY1))


        if keycode in ['KEY_ENTER', 'KEY_PLAYPAUSE']:
            self._speed = [0, 0]

        if keycode in ['KEY_UP', 'KEY_VOLUMEUP']:
            self._speed = [self._base_speed[0], self._base_speed[1]]

        if keycode in ['KEY_DOWN', 'KEY_VOLUMEDOWN']:
            self._speed = [-self._base_speed[0], -self._base_speed[1]]

        if keycode == 'KEY_LEFT':
            self._dc_mtr.send_cmdline('speed %s %s' %
                                      (self._speed[0] - self.ROT_STEP,
                                       self._speed[1] + self.ROT_STEP))
            self._dc_mtr.send_cmdline('delay %s' % (self.DELAY_TURN))

        if keycode == 'KEY_RIGHT':
            self._dc_mtr.send_cmdline('speed %s %s' %
                                      (self._speed[0] + self.ROT_STEP,
                                       self._speed[1] - self.ROT_STEP))
            self._dc_mtr.send_cmdline('delay %s' % (self.DELAY_TURN))

        if keycode == 'KEY_PREVIOUSSONG':
            self._speed = [0, self._base_speed[1]]

        if keycode == 'KEY_NEXTSONG':
            self._speed = [self._base_speed[0], 0]

        #
        if keycode == 'BTN_LEFT':
            self._base_speed[0] = self.speed_add1(self._base_speed[0],
                                                  self.CALIB_STEP)
            d_speed = [self.CALIB_STEP, 0]

        if keycode == 'BTN_RIGHT':
            self._base_speed[0] = self.speed_add1(self._base_speed[0],
                                                  -self.CALIB_STEP)
            d_speed = [-self.CALIB_STEP, 0]

        if keycode == 'KEY_PAGEUP':
            self._base_speed[1] = self.speed_add1(self._base_speed[1],
                                                  self.CALIB_STEP)
            d_speed = [0, self.CALIB_STEP]

        if keycode == 'KEY_PAGEDOWN':
            self._base_speed[1] = self.speed_add1(self._base_speed[1],
                                                  -self.CALIB_STEP)
            d_speed = [0, -self.CALIB_STEP]

        # move
        self.speed_add(d_speed)
        self._dc_mtr.send_cmdline('speed %s %s' % tuple(self._speed))

        self._prev_keycode = keycode
        self._prev_keyval = keyval


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

    dc_mtr = DcMtrClient(svr_host, svr_port, obj['debug'] or debug)
    test_app = Test_RobotTank(devs, dc_mtr, obj['debug'] or debug)

    try:
        test_app.main()

    finally:
        dc_mtr.send_cmdline('stop')
        print('END')
