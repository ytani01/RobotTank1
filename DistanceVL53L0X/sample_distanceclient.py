#!/usr/bin/env python3
#
# Copyright (c) 2023 Yoichi Tanibayahshi
#
# -*- coding: utf-8 -*-
#
import click
import time
import datetime
from distancevl53l0x import DistanceClient, get_logger


DEF_HOST = 'localhost'
DEF_PORT = 12347
DEF_DELAY = 0.1


@click.command(context_settings=dict(help_option_names=['-h', '--help']),
               help='Sample Distance Client')
@click.option('--svr_host', '--host', '-s', 'svr_host',
              type=str, default=DEF_HOST,
              help='server host name (default:%s)' % (DEF_HOST))
@click.option('--svr_port', '--port', '-p', 'svr_port',
              type=int, default=DEF_PORT,
              help='server port number (default:%s)' % (DEF_PORT))
@click.option('--delay', '-t', 'delay', type=float, default=DEF_DELAY,
              help='delay sec (default: %s)' % (DEF_DELAY))
@click.option('--debug', '-d', 'debug', is_flag=True, default=False,
              help='')
def main(svr_host, svr_port, delay, debug):
    __log = get_logger(__name__, debug)
    __log.debug('server %s:%s, delay=%s', svr_host, svr_port, delay)

    dc = DistanceClient('localhost', 12347, debug=debug)

    while True:
        tm = datetime.datetime.now().strftime('%H:%M:%S.%f')
        distance = dc.get_distance()
        graph_str = '*' * int(distance / 10)

        print('%s: %4d %s' % (tm, distance, graph_str))

        time.sleep(delay)


if __name__ == '__main__':
    main()
