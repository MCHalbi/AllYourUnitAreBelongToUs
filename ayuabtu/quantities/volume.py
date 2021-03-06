# Author: Lukas Halbritter <halbritl@informatik.uni-freiburg.de>
# Copyright 2020
from ..units import VolumeUnit


class Volume:
    base_unit = VolumeUnit.CUBICMETER
    factors = {
        VolumeUnit.CUBICMETER: 1,
    }
    abbreviations = {
        VolumeUnit.CUBICMETER: 'm³',
    }

    def __init__(self, value: float, unit: 'VolumeUnit') -> None:
        self._value = value
        self._unit = unit

    def __str__(self):
        return "{value} {unit}".format(
            value=str(self._value),
            unit=Volume.abbreviations[self._unit])

    def __repr__(self):
        return str(self)

    # Comparison operators
    def __eq__(self, other):
        return self._value == other.as_unit(self._unit)

    # Unary operators
    def __neg__(self):
        return Volume(-self._value, self._unit)

    # Arithmetic operators
    def __add__(self, other):
        if type(other) is Volume:
            return Volume(self._value + other.as_unit(self._unit), self._unit)

        self._raise_type_error_for_undefined_operator(other, '+')

    def __sub__(self, other):
        if type(other) is Volume:
            return Volume(self._value - other.as_unit(self._unit), self._unit)

        self._raise_type_error_for_undefined_operator(other, '-')

    def __mul__(self, other):

        if type(other) in (float, int):
            result = Volume(self._value * other, self._unit)
        else:
            self._raise_type_error_for_undefined_operator(other, '*')

        return result

    def __rmul__(self, other):

        if type(other) in (float, int, ):
            return self * other

        self._raise_type_error_for_undefined_operator(other, '*')

    def __truediv__(self, other):
        from .length import Length
        from .area import Area

        if type(other) is Volume:
            result = (self._get_value_in_base_unit()
                    / other.as_unit(other.base_unit))
        elif type(other) in (float, int):
            result = Volume(self._value / other, self._unit)
        elif type(other) is Length:
            result = Area(
                self.as_unit(self.base_unit) / other.as_unit(other.base_unit),
                Area.base_unit)
        elif type(other) is Area:
            result = Length(
                self.as_unit(self.base_unit) / other.as_unit(other.base_unit),
                Length.base_unit)
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
    def zero() -> 'Volume':
        return Volume(0, Volume.base_unit)

    @property
    def unit(self) -> VolumeUnit:
        return self._unit

    @property
    def value(self) -> float:
        return self._value

    def as_unit(self, unit: VolumeUnit) -> float:
        if unit == self._unit:
            return self._value

        return self._get_value_as(unit)

    def to_unit(self, unit: VolumeUnit) -> 'Volume':
        converted_value = self._get_value_as(unit)

        return Volume(converted_value, unit)

    # Generation shorthands
    @staticmethod
    def from_cubicMeters(value: float) -> 'Volume':
        return Volume(value, VolumeUnit.CUBICMETER)

    # Conversion shorthands
    @property
    def cubicMeters(self) -> float:
        return self.as_unit(VolumeUnit.CUBICMETER)

    def _to_base_unit(self) -> 'Volume':
        return self.to_unit(self.base_unit)

    def _get_value_in_base_unit(self) -> float:
        try:
            return self._value * Volume.factors[self._unit]
        except KeyError:
            raise NotImplementedError(
                'Can not convert {0} to base units.'.format(self._unit.name))

    def _get_value_as(self, unit: VolumeUnit) -> float:
        base_unit_value = self._get_value_in_base_unit()

        try:
            return base_unit_value / Volume.factors[unit]
        except KeyError:
            raise NotImplementedError(
                'Can not convert {0} to {1}.'.format(self._unit.name, unit))
