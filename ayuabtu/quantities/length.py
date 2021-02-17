# This file was created automatically. Every change made in this file will be
# lost when the package is built the next time.
#
# Author: Lukas Halbritter <halbritl@informatik.uni-freiburg.de>
# Copyright 2020 - 2021
from ..units import LengthUnit


class Length:
    base_unit = LengthUnit.METER
    factors = {
        LengthUnit.ASTRONOMICALUNIT: 1.4959787070e11,
        LengthUnit.CENTIMETER: 1e-2,
        LengthUnit.CHAIN: 20.1168,
        LengthUnit.DECAMETER: 1e1,
        LengthUnit.DECIMETER: 1e-1,
        LengthUnit.DTPPICA: 1 / 236.220472441,
        LengthUnit.DTPPOINT: 2.54e-2 / 72,
        LengthUnit.FATHOM: 1.8288,
        LengthUnit.FOOT: 0.3048,
        LengthUnit.HAND: 1.016e-1,
        LengthUnit.HECTOMETER: 1e2,
        LengthUnit.INCH: 0.0254,
        LengthUnit.KILOLIGHTYEAR: 9.4607304725808e18,
        LengthUnit.KILOMETER: 1e3,
        LengthUnit.KILOPARSEC: 3.085677581e19,
        LengthUnit.LIGHTYEAR: 9.4607304725808e15,
        LengthUnit.MEGALIGHTYEAR: 9.4607304725808e21,
        LengthUnit.MEGAPARSEC: 3.085677581e22,
        LengthUnit.METER: 1,
        LengthUnit.MICROINCH: 2.54e-8,
        LengthUnit.MICROMETER: 1e-6,
        LengthUnit.MIL: 2.54e-5,
        LengthUnit.MILE: 1609.34,
        LengthUnit.MILLIMETER: 1e-3,
        LengthUnit.NANOMETER: 1e-9,
        LengthUnit.NAUTICALMILE: 1852,
        LengthUnit.PARSEC: 3.085677581e16,
        LengthUnit.SHACKLE: 27.432,
        LengthUnit.SOLARRADIUS: 6.96342e8,
        LengthUnit.TWIP: 1 / 56692.913385826,
        LengthUnit.USSURVEYFOOT: 1200 / 3937,
        LengthUnit.YARD: 0.9144,
    }
    abbreviations = {
        LengthUnit.ASTRONOMICALUNIT: 'au',
        LengthUnit.CENTIMETER: 'cm',
        LengthUnit.CHAIN: 'ch',
        LengthUnit.DECAMETER: 'dam',
        LengthUnit.DECIMETER: 'dm',
        LengthUnit.DTPPICA: 'pica',
        LengthUnit.DTPPOINT: 'pt',
        LengthUnit.FATHOM: 'fathom',
        LengthUnit.FOOT: 'ft',
        LengthUnit.HAND: 'h',
        LengthUnit.HECTOMETER: 'hm',
        LengthUnit.INCH: 'in',
        LengthUnit.KILOLIGHTYEAR: 'kly',
        LengthUnit.KILOMETER: 'km',
        LengthUnit.KILOPARSEC: 'kpc',
        LengthUnit.LIGHTYEAR: 'ly',
        LengthUnit.MEGALIGHTYEAR: 'Mly',
        LengthUnit.MEGAPARSEC: 'Mpc',
        LengthUnit.METER: 'm',
        LengthUnit.MICROINCH: 'μin',
        LengthUnit.MICROMETER: 'μm',
        LengthUnit.MIL: 'mil',
        LengthUnit.MILE: 'mi',
        LengthUnit.MILLIMETER: 'mm',
        LengthUnit.NANOMETER: 'nm',
        LengthUnit.NAUTICALMILE: 'NM',
        LengthUnit.PARSEC: 'pc',
        LengthUnit.SHACKLE: 'shackle',
        LengthUnit.SOLARRADIUS: 'R⊙',
        LengthUnit.TWIP: 'twip',
        LengthUnit.USSURVEYFOOT: 'ft (U.S.)',
        LengthUnit.YARD: 'yd',
    }

    def __init__(self, value: float, unit: 'LengthUnit') -> None:
        self._value = value
        self._unit = unit

    def __str__(self):
        return "{value} {unit}".format(
            value=str(self._value),
            unit=Length.abbreviations[self._unit])

    def __repr__(self):
        return str(self)

    # Comparison operators
    def __eq__(self, other):
        return self._value == other.as_unit(self._unit)

    # Unary operators
    def __neg__(self):
        return Length(-self._value, self._unit)

    # Arithmetic operators
    def __add__(self, other):
        if type(other) is Length:
            return Length(self._value + other.as_unit(self._unit), self._unit)

        self._raise_type_error_for_undefined_operator(other, '+')

    def __sub__(self, other):
        if type(other) is Length:
            return Length(self._value - other.as_unit(self._unit), self._unit)

        self._raise_type_error_for_undefined_operator(other, '-')

    def __mul__(self, other):
        from .volume import Volume
        from .area import Area

        if type(other) in (float, int):
            result = Length(self._value * other, self._unit)
        elif type(other) is Length:
            result = Area(
                self.as_unit(self.base_unit) * other.as_unit(other.base_unit),
                Area.base_unit)
        elif type(other) is Area:
            result = Volume(
                self.as_unit(self.base_unit) * other.as_unit(other.base_unit),
                Volume.base_unit)
        else:
            self._raise_type_error_for_undefined_operator(other, '*')

        return result

    def __rmul__(self, other):
        from .volume import Volume
        from .area import Area

        if type(other) in (float, int, Length, Area):
            return self * other

        self._raise_type_error_for_undefined_operator(other, '*')

    def __truediv__(self, other):

        if type(other) is Length:
            result = (self._get_value_in_base_unit()
                    / other.as_unit(other.base_unit))
        elif type(other) in (float, int):
            result = Length(self._value / other, self._unit)
        else:
            self._raise_type_error_for_undefined_operator(other, '/')

        return result

    def __pow__(self, other):
        if type(other) in (float, int):
            result = 1
            for _ in range(other):
              result *= self

            return result
        else:
            self._raise_type_error_for_undefined_operator(other, '**')

    def _raise_type_error_for_undefined_operator(
            self, other, operator: str) -> None:
        raise TypeError(
            'unsupported operand type(s) for {0}: \'{1}\' and \'{2}\''
            .format(operator, type(self).__name__, type(other).__name__))

    @staticmethod
    def zero() -> 'Length':
        return Length(0, Length.base_unit)

    @property
    def unit(self) -> LengthUnit:
        return self._unit

    @property
    def value(self) -> float:
        return self._value

    def as_unit(self, unit: LengthUnit) -> float:
        if unit == self._unit:
            return self._value

        return self._get_value_as(unit)

    def to_unit(self, unit: LengthUnit) -> 'Length':
        converted_value = self._get_value_as(unit)

        return Length(converted_value, unit)

    # Generation shorthands
    @staticmethod
    def from_astronomical_units(value: float) -> 'Length':
        return Length(value, LengthUnit.ASTRONOMICALUNIT)

    @staticmethod
    def from_centimeters(value: float) -> 'Length':
        return Length(value, LengthUnit.CENTIMETER)

    @staticmethod
    def from_chains(value: float) -> 'Length':
        return Length(value, LengthUnit.CHAIN)

    @staticmethod
    def from_decameters(value: float) -> 'Length':
        return Length(value, LengthUnit.DECAMETER)

    @staticmethod
    def from_decimeters(value: float) -> 'Length':
        return Length(value, LengthUnit.DECIMETER)

    @staticmethod
    def from_dtp_picas(value: float) -> 'Length':
        return Length(value, LengthUnit.DTPPICA)

    @staticmethod
    def from_dtp_points(value: float) -> 'Length':
        return Length(value, LengthUnit.DTPPOINT)

    @staticmethod
    def from_fathoms(value: float) -> 'Length':
        return Length(value, LengthUnit.FATHOM)

    @staticmethod
    def from_feet(value: float) -> 'Length':
        return Length(value, LengthUnit.FOOT)

    @staticmethod
    def from_hands(value: float) -> 'Length':
        return Length(value, LengthUnit.HAND)

    @staticmethod
    def from_hectometers(value: float) -> 'Length':
        return Length(value, LengthUnit.HECTOMETER)

    @staticmethod
    def from_inches(value: float) -> 'Length':
        return Length(value, LengthUnit.INCH)

    @staticmethod
    def from_kilolight_years(value: float) -> 'Length':
        return Length(value, LengthUnit.KILOLIGHTYEAR)

    @staticmethod
    def from_kilometers(value: float) -> 'Length':
        return Length(value, LengthUnit.KILOMETER)

    @staticmethod
    def from_kiloparsecs(value: float) -> 'Length':
        return Length(value, LengthUnit.KILOPARSEC)

    @staticmethod
    def from_light_years(value: float) -> 'Length':
        return Length(value, LengthUnit.LIGHTYEAR)

    @staticmethod
    def from_megalight_years(value: float) -> 'Length':
        return Length(value, LengthUnit.MEGALIGHTYEAR)

    @staticmethod
    def from_megaparsecs(value: float) -> 'Length':
        return Length(value, LengthUnit.MEGAPARSEC)

    @staticmethod
    def from_meters(value: float) -> 'Length':
        return Length(value, LengthUnit.METER)

    @staticmethod
    def from_microinches(value: float) -> 'Length':
        return Length(value, LengthUnit.MICROINCH)

    @staticmethod
    def from_micrometers(value: float) -> 'Length':
        return Length(value, LengthUnit.MICROMETER)

    @staticmethod
    def from_mils(value: float) -> 'Length':
        return Length(value, LengthUnit.MIL)

    @staticmethod
    def from_miles(value: float) -> 'Length':
        return Length(value, LengthUnit.MILE)

    @staticmethod
    def from_millimeters(value: float) -> 'Length':
        return Length(value, LengthUnit.MILLIMETER)

    @staticmethod
    def from_nanometers(value: float) -> 'Length':
        return Length(value, LengthUnit.NANOMETER)

    @staticmethod
    def from_nautical_miles(value: float) -> 'Length':
        return Length(value, LengthUnit.NAUTICALMILE)

    @staticmethod
    def from_parsecs(value: float) -> 'Length':
        return Length(value, LengthUnit.PARSEC)

    @staticmethod
    def from_shackles(value: float) -> 'Length':
        return Length(value, LengthUnit.SHACKLE)

    @staticmethod
    def from_solar_radii(value: float) -> 'Length':
        return Length(value, LengthUnit.SOLARRADIUS)

    @staticmethod
    def from_twips(value: float) -> 'Length':
        return Length(value, LengthUnit.TWIP)

    @staticmethod
    def from_us_survey_feet(value: float) -> 'Length':
        return Length(value, LengthUnit.USSURVEYFOOT)

    @staticmethod
    def from_yards(value: float) -> 'Length':
        return Length(value, LengthUnit.YARD)

    # Conversion shorthands
    @property
    def astronomical_units(self) -> float:
        return self.as_unit(LengthUnit.ASTRONOMICALUNIT)

    @property
    def centimeters(self) -> float:
        return self.as_unit(LengthUnit.CENTIMETER)

    @property
    def chains(self) -> float:
        return self.as_unit(LengthUnit.CHAIN)

    @property
    def decameters(self) -> float:
        return self.as_unit(LengthUnit.DECAMETER)

    @property
    def decimeters(self) -> float:
        return self.as_unit(LengthUnit.DECIMETER)

    @property
    def dtp_picas(self) -> float:
        return self.as_unit(LengthUnit.DTPPICA)

    @property
    def dtp_points(self) -> float:
        return self.as_unit(LengthUnit.DTPPOINT)

    @property
    def fathoms(self) -> float:
        return self.as_unit(LengthUnit.FATHOM)

    @property
    def feet(self) -> float:
        return self.as_unit(LengthUnit.FOOT)

    @property
    def hands(self) -> float:
        return self.as_unit(LengthUnit.HAND)

    @property
    def hectometers(self) -> float:
        return self.as_unit(LengthUnit.HECTOMETER)

    @property
    def inches(self) -> float:
        return self.as_unit(LengthUnit.INCH)

    @property
    def kilolight_years(self) -> float:
        return self.as_unit(LengthUnit.KILOLIGHTYEAR)

    @property
    def kilometers(self) -> float:
        return self.as_unit(LengthUnit.KILOMETER)

    @property
    def kiloparsecs(self) -> float:
        return self.as_unit(LengthUnit.KILOPARSEC)

    @property
    def light_years(self) -> float:
        return self.as_unit(LengthUnit.LIGHTYEAR)

    @property
    def megalight_years(self) -> float:
        return self.as_unit(LengthUnit.MEGALIGHTYEAR)

    @property
    def megaparsecs(self) -> float:
        return self.as_unit(LengthUnit.MEGAPARSEC)

    @property
    def meters(self) -> float:
        return self.as_unit(LengthUnit.METER)

    @property
    def microinches(self) -> float:
        return self.as_unit(LengthUnit.MICROINCH)

    @property
    def micrometers(self) -> float:
        return self.as_unit(LengthUnit.MICROMETER)

    @property
    def mils(self) -> float:
        return self.as_unit(LengthUnit.MIL)

    @property
    def miles(self) -> float:
        return self.as_unit(LengthUnit.MILE)

    @property
    def millimeters(self) -> float:
        return self.as_unit(LengthUnit.MILLIMETER)

    @property
    def nanometers(self) -> float:
        return self.as_unit(LengthUnit.NANOMETER)

    @property
    def nautical_miles(self) -> float:
        return self.as_unit(LengthUnit.NAUTICALMILE)

    @property
    def parsecs(self) -> float:
        return self.as_unit(LengthUnit.PARSEC)

    @property
    def shackles(self) -> float:
        return self.as_unit(LengthUnit.SHACKLE)

    @property
    def solar_radii(self) -> float:
        return self.as_unit(LengthUnit.SOLARRADIUS)

    @property
    def twips(self) -> float:
        return self.as_unit(LengthUnit.TWIP)

    @property
    def us_survey_feet(self) -> float:
        return self.as_unit(LengthUnit.USSURVEYFOOT)

    @property
    def yards(self) -> float:
        return self.as_unit(LengthUnit.YARD)

    def _to_base_unit(self) -> 'Length':
        return self.to_unit(self.base_unit)

    def _get_value_in_base_unit(self) -> float:
        try:
            return self._value * Length.factors[self._unit]
        except KeyError:
            raise NotImplementedError(
                'Can not convert {0} to base units.'.format(self._unit.name))

    def _get_value_as(self, unit: LengthUnit) -> float:
        base_unit_value = self._get_value_in_base_unit()

        try:
            return base_unit_value / Length.factors[unit]
        except KeyError:
            raise NotImplementedError(
                'Can not convert {0} to {1}.'.format(self._unit.name, unit))
