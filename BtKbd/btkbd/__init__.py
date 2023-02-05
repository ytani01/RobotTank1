#
# Copyright (c) 2023 Yoichi Tanibayashi
#
__prog_name__ = 'btkbd'
__version__ = '0.0.1'
__author__ = 'Yoichi Tanibayashi'

from .btkbd import BtKbd

from .test_kbd import kbd
from .test_robottank import robottank

from .my_logger import get_logger

all = [__prog_name__, __version__, __author__,
       'BtKbd',
       'kbd',
       'robottank',
       'get_logger']
