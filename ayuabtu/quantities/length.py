# Author: Lukas Halbritter <halbritl@informatik.uni-freiburg.de>
# Copyright 2020
from ..units import LengthUnit


class Length:
    base_unit = LengthUnit.METER
    factors = {
        LengthUnit.KILOMETER: 1e3,
        LengthUnit.HECTOMETER: 1e2,
        LengthUnit.DECAMETER: 1e1,
        LengthUnit.METER: 1e0,
        LengthUnit.DECIMETER: 1e-1,
        LengthUnit.CENTIMETER: 1e-2,
        LengthUnit.MILLIMETER: 1e-3,
        LengthUnit.MICROMETER: 1e-6,
        LengthUnit.NANOMETER: 1e-9,
        LengthUnit.INCH: 0.0254,
        LengthUnit.FOOT: 0.3048,
        LengthUnit.YARD: 0.9144,
        LengthUnit.MILE: 1609.34,
    }
    abbreviations = {
        LengthUnit.KILOMETER: 'km',
        LengthUnit.HECTOMETER: 'hm',
        LengthUnit.DECAMETER: 'dam',
        LengthUnit.METER: 'm',
        LengthUnit.DECIMETER: 'dm',
        LengthUnit.CENTIMETER: 'cm',
        LengthUnit.MILLIMETER: 'mm',
        LengthUnit.MICROMETER: 'μm',
        LengthUnit.NANOMETER: 'nm',
        LengthUnit.INCH: 'in',
        LengthUnit.FOOT: 'ft',
        LengthUnit.YARD: 'yd',
        LengthUnit.MILE: 'mi',
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
        if type(other) in (float, int):
            return Length(self._value * other, self._unit)

        self._raise_type_error_for_undefined_operator(other, '*')

    def __rmul__(self, other):
        if type(other) in (float, int):
            return self * other

        self._raise_type_error_for_undefined_operator(other, '*')

    def __truediv__(self, other):
        if type(other) is Length:
            return (self._get_value_in_base_unit()
                    / other.as_unit(other.base_unit))
        if type(other) in (float, int):
            return Length(self._value / other, self._unit)

        self._raise_type_error_for_undefined_operator(other, '/')

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