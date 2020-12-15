# Author: Lukas Halbritter <halbritl@informatik.uni-freiburg.de>
# Copyright 2020
from enum import Enum


class MassUnit(Enum):
    GIGATONNE = 0
    MEGATONNE = 1
    KILOTONNE = 2
    TONNE = 3
    KILOGRAM = 4
    HECTOGRAM = 5
    DECAGRAM = 6
    GRAM = 7
    DECIGRAM = 8
    CENTIGRAM = 9
    MILLIGRAM = 10
    MICROGRAM = 11
    NANOGRAM = 12
    MEGAPOUND = 13
    KILOPOUND = 14
    POUND = 15
    OUNCE = 16
    GRAIN = 17
    SHORTHUNDREDWEIGHT = 18
    SHORTTON = 19
    STONE = 20
    LONGHUNDREDWEIGHT = 21
    LONGTON = 22
    EARTHMASS = 23
    SOLARMASS = 24
