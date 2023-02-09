#
# Copyright (c) 2023 Yoichi Tanibayashi
#
__prog_name__ = 'btserial'
__version__ = '0.0.1'
__author__ = 'Yoichi Tanibayashi'

from .btsersvr import BtSerSvr

from .test_btsersvr import btsersvr
# from .test_robottank import robottank

from .my_logger import get_logger

all = [__prog_name__, __version__, __author__,
       'BtSerSvr',
       'btsersvr',
       'robottank',
       'get_logger']
