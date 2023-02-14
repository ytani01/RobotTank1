#!/usr/bin/env python3

import struct


DEVFILE = '/dev/input/js0'
EV_FORMAT = "LhBB"
EV_SIZE = struct.calcsize(EV_FORMAT)

with open(DEVFILE, "rb") as dev:
    while True:
        ev = dev.read(EV_SIZE)
        (tm, v, ty, n) = struct.unpack(EV_FORMAT, ev)
        print("%s, %s, %s, %s" % (tm, v, ty, n))
