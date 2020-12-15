# Author: Lukas Halbritter <halbritl@informatik.uni-freiburg.de>
# Copyright 2020
from enum import Enum


class TimeUnit(Enum):
    WEEK = 0
    DAY = 1
    HOUR = 2
    MINUTE = 3
    SECOND = 4
    MILLISECOND = 5
    MICROSECOND = 6
    NANOSECOND = 7
