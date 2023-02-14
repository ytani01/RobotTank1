#
# Copyright (c) 2023 Yoichi Tanibayashi
#
__prog_name__ = 'bt8bitdozero2'
__version__ = '0.0.1'
__author__ = 'Yoichi Tanibayashi'

from .bt8bitdozero2 import Bt8BitDoZero2

from .test_bt8bitdozero2 import bt8bitdozero2
from .test_robottank import robottank

from .my_logger import get_logger

all = [__prog_name__, __version__, __author__,
       'Bt8BitDoZero2',
       'bt8bitdozero2',
       'robottank',
       'get_logger']
