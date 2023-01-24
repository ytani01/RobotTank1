#
# Copyright (c) 2023 Yoichi Tanibayashi
#
__prog_name__ = 'robottank'
__version__ = '0.0.1'
__author__ = 'Yoichi Tanibayashi'

from .dc_mtr import DcMtr
from .my_logger import get_logger

all = ['DcMtr',
       'get_logger', __prog_name__, __version__, __author__]
