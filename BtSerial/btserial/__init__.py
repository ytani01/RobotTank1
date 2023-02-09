#
# Copyright (c) 2023 Yoichi Tanibayashi
#
__prog_name__ = 'btserial'
__version__ = '0.0.1'
__author__ = 'Yoichi Tanibayashi'

from .btserial import BtSerial

from .test_btsvr import btsvr
from .test_robottank import robottank

from .my_logger import get_logger

all = [__prog_name__, __version__, __author__,
       'BtSerial',
       'btsvr',
       'robottank',
       'get_logger']
