# Author: Lukas Halbritter <halbritl@informatik.uni-freiburg.de>
# Copyright 2020
from enum import Enum


class LengthUnit(Enum):
    # SI
    KILOMETER = 0
    HECTOMETER = 1
    DECAMETER = 2
    METER = 3
    DECIMETER = 4
    CENTIMETER = 5
    MILLIMETER = 6
    MICROMETER = 7
    NANOMETER = 8

    # Imperial
    INCH = 9
    FOOT = 10
    YARD = 11
    MILE = 12
