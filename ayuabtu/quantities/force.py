# This file was created automatically. Every change made in this file will be
# lost when the package is built the next time.
#
# Author: Lukas Halbritter <halbritl@informatik.uni-freiburg.de>
# Copyright 2020 - 2021
from ..units import ForceUnit


class Force:
    base_unit = ForceUnit.NEWTON
    factors = {
        ForceUnit.DYN: 1e-5,
        ForceUnit.NEWTON: 1,
    }
    abbreviations = {
        ForceUnit.DYN: 'dyn',
        ForceUnit.NEWTON: 'N',
    }

    def __init__(self, value: float, unit: 'ForceUnit') -> None:
        self._value = value
        self._unit = unit

    def __str__(self):
        return "{value} {unit}".format(
            value=str(self._value),
            unit=Force.abbreviations[self._unit])

    def __repr__(self):
        return str(self)

    # Comparison operators
    def __eq__(self, other):
        return self._value == other.as_unit(self._unit)

    # Unary operators
    def __neg__(self):
        return Force(-self._value, self._unit)

    # Arithmetic operators
    def __add__(self, other):
        if type(other) is Force:
            return Force(self._value + other.as_unit(self._unit), self._unit)

        self._raise_type_error_for_undefined_operator(other, '+')

    def __sub__(self, other):
        if type(other) is Force:
            return Force(self._value - other.as_unit(self._unit), self._unit)

        self._raise_type_error_for_undefined_operator(other, '-')

    def __mul__(self, other):

        if type(other) in (float, int):
            result = Force(self._value * other, self._unit)
        else:
            self._raise_type_error_for_undefined_operator(other, '*')

        return result

    def __rmul__(self, other):

        if type(other) in (float, int, ):
            return self * other

        self._raise_type_error_for_undefined_operator(other, '*')

    def __truediv__(self, other):

        if type(other) is Force:
            result = (self._get_value_in_base_unit()
                    / other.as_unit(other.base_unit))
        elif type(other) in (float, int):
            result = Force(self._value / other, self._unit)
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
    def zero() -> 'Force':
        return Force(0, Force.base_unit)

    @property
    def unit(self) -> ForceUnit:
        return self._unit

    @property
    def value(self) -> float:
        return self._value

    def as_unit(self, unit: ForceUnit) -> float:
        if unit == self._unit:
            return self._value

        return self._get_value_as(unit)

    def to_unit(self, unit: ForceUnit) -> 'Force':
        converted_value = self._get_value_as(unit)

        return Force(converted_value, unit)

    # Generation shorthands
    @staticmethod
    def from_dyns(value: float) -> 'Force':
        return Force(value, ForceUnit.DYN)

    @staticmethod
    def from_newtons(value: float) -> 'Force':
        return Force(value, ForceUnit.NEWTON)

    # Conversion shorthands
    @property
    def dyns(self) -> float:
        return self.as_unit(ForceUnit.DYN)

    @property
    def newtons(self) -> float:
        return self.as_unit(ForceUnit.NEWTON)

    def _to_base_unit(self) -> 'Force':
        return self.to_unit(self.base_unit)

    def _get_value_in_base_unit(self) -> float:
        try:
            return self._value * Force.factors[self._unit]
        except KeyError:
            raise NotImplementedError(
                'Can not convert {0} to base units.'.format(self._unit.name))

    def _get_value_as(self, unit: ForceUnit) -> float:
        base_unit_value = self._get_value_in_base_unit()

        try:
            return base_unit_value / Force.factors[unit]
        except KeyError:
            raise NotImplementedError(
                'Can not convert {0} to {1}.'.format(self._unit.name, unit))
