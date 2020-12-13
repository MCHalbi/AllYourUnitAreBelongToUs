# Author: Lukas Halbritter <halbritl@informatik.uni-freiburg.de>
# Copyright 2020
from ..units import MassUnit


class Mass:
    base_unit = MassUnit.KILOGRAM
    factors = {
        MassUnit.GIGATONNE: 1e12,
        MassUnit.MEGATONNE: 1e9,
        MassUnit.KILOTONNE: 1e6,
        MassUnit.TONNE: 1e3,
        MassUnit.KILOGRAM: 1e0,
        MassUnit.HECTOGRAM: 1e-1,
        MassUnit.DECAGRAM: 1e-2,
        MassUnit.GRAM: 1e-3,
        MassUnit.DECIGRAM: 1e-4,
        MassUnit.CENTIGRAM: 1e-5,
        MassUnit.MILLIGRAM: 1e-6,
        MassUnit.MICROGRAM: 1e-9,
        MassUnit.NANOGRAM: 1e-12,
        MassUnit.MEGAPOUND: 4.53592370e5,
        MassUnit.KILOPOUND: 4.53592370e2,
        MassUnit.POUND: 4.53592370e-1,
        MassUnit.OUNCE: 2.8349523125e-2,
        MassUnit.GRAIN: 6.479891e-5,
        MassUnit.SHORTHUNDREDWEIGHT: 45.359237,
        MassUnit.SHORTTON: 907.18474,
        MassUnit.STONE: 6.35029318,
        MassUnit.LONGHUNDREDWEIGHT: 50.80234544,
        MassUnit.LONGTON: 1016.0469088,
        MassUnit.EARTHMASS: 5.9723e24,
        MassUnit.SOLARMASS: 1.98892e30,
    }
    abbreviations = {
        MassUnit.GIGATONNE: 'Gt',
        MassUnit.MEGATONNE: 'Mt',
        MassUnit.KILOTONNE: 'kt',
        MassUnit.TONNE: 't',
        MassUnit.KILOGRAM: 'kg',
        MassUnit.HECTOGRAM: 'hg',
        MassUnit.DECAGRAM: 'dag',
        MassUnit.GRAM: 'g',
        MassUnit.DECIGRAM: 'dg',
        MassUnit.CENTIGRAM: 'cg',
        MassUnit.MILLIGRAM: 'mg',
        MassUnit.MICROGRAM: 'μg',
        MassUnit.NANOGRAM: 'ng',
        MassUnit.MEGAPOUND: 'Mlb.',
        MassUnit.KILOPOUND: 'klb.',
        MassUnit.POUND: 'lb.',
        MassUnit.OUNCE: 'oz.',
        MassUnit.GRAIN: 'gr.',
        MassUnit.SHORTHUNDREDWEIGHT: 'cwt.',
        MassUnit.SHORTTON: 'to.',
        MassUnit.STONE: 'st.',
        MassUnit.LONGHUNDREDWEIGHT: 'cwt.',
        MassUnit.LONGTON: 'to.',
        MassUnit.EARTHMASS: 'M⊕',
        MassUnit.SOLARMASS: 'M☉',
    }

    def __init__(self, value: float, unit: 'MassUnit') -> None:
        self._value = value
        self._unit = unit

    def __str__(self):
        return "{value} {unit}".format(
            value=str(self._value),
            unit=Mass.abbreviations[self._unit])

    def __repr__(self):
        return str(self)

    # Comparison operators
    def __eq__(self, other):
        return self._value == other.as_unit(self._unit)

    # Unary operators
    def __neg__(self):
        return Mass(-self._value, self._unit)

    # Arithmetic operators
    def __add__(self, other):
        if type(other) is Mass:
            return Mass(self._value + other.as_unit(self._unit), self._unit)

        self._raise_type_error_for_undefined_operator(other, '+')

    def __sub__(self, other):
        if type(other) is Mass:
            return Mass(self._value - other.as_unit(self._unit), self._unit)

        self._raise_type_error_for_undefined_operator(other, '-')

    def __mul__(self, other):
        if type(other) in (float, int):
            return Mass(self._value * other, self._unit)

        self._raise_type_error_for_undefined_operator(other, '*')

    def __rmul__(self, other):
        if type(other) in (float, int):
            return self * other

        self._raise_type_error_for_undefined_operator(other, '*')

    def __truediv__(self, other):
        if type(other) is Mass:
            return (self._get_value_in_base_unit()
                    / other.as_unit(other.base_unit))
        if type(other) in (float, int):
            return Mass(self._value / other, self._unit)

        self._raise_type_error_for_undefined_operator(other, '/')

    def _raise_type_error_for_undefined_operator(
            self, other, operator: str) -> None:
        raise TypeError(
            'unsupported operand type(s) for {0}: \'{1}\' and \'{2}\''
            .format(operator, type(self).__name__, type(other).__name__))

    @staticmethod
    def zero() -> 'Mass':
        return Mass(0, Mass.base_unit)

    @property
    def unit(self) -> MassUnit:
        return self._unit

    @property
    def value(self) -> float:
        return self._value

    def as_unit(self, unit: MassUnit) -> float:
        if unit == self._unit:
            return self._value

        return self._get_value_as(unit)

    def to_unit(self, unit: MassUnit) -> 'Mass':
        converted_value = self._get_value_as(unit)

        return Mass(converted_value, unit)

    def _to_base_unit(self) -> 'Mass':
        return self.to_unit(self.base_unit)

    def _get_value_in_base_unit(self) -> float:
        try:
            return self._value * Mass.factors[self._unit]
        except KeyError:
            raise NotImplementedError(
                'Can not convert {0} to base units.'.format(self._unit.name))

    def _get_value_as(self, unit: MassUnit) -> float:
        base_unit_value = self._get_value_in_base_unit()

        try:
            return base_unit_value / Mass.factors[unit]
        except KeyError:
            raise NotImplementedError(
                'Can not convert {0} to {1}.'.format(self._unit.name, unit))
