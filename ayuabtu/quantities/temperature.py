# This file was created automatically. Every change made in this file will be
# lost when the package is built the next time.
#
# Author: Lukas Halbritter <halbritl@informatik.uni-freiburg.de>
# Copyright 2020 - 2021
from ..units import TemperatureUnit


class Temperature:
    base_unit = TemperatureUnit.KELVIN
    factors = {
        TemperatureUnit.KELVIN: 1,
        TemperatureUnit.DEGREEFAHRENHEIT: 5 / 9,
        TemperatureUnit.DEGREECELSIUS: 1,
        TemperatureUnit.DEGREERANKINE: 5 / 9,
        TemperatureUnit.DEGREEDELISLE: - 2 / 3,
        TemperatureUnit.DEGREENEWTON: 100/33,
        TemperatureUnit.DEGREEREAUMUR: 1.25,
        TemperatureUnit.DEGREEROEMER: 40 / 21,
    }
    offsets = {
        TemperatureUnit.KELVIN: 0,
        TemperatureUnit.DEGREEFAHRENHEIT: 2298.35 / 9,
        TemperatureUnit.DEGREECELSIUS: 237.15,
        TemperatureUnit.DEGREERANKINE: 0,
        TemperatureUnit.DEGREEDELISLE: 375.15,
        TemperatureUnit.DEGREENEWTON: 273.15,
        TemperatureUnit.DEGREEREAUMUR: 273.15,
        TemperatureUnit.DEGREEROEMER: 5448.15 / 21,
    }
    abbreviations = {
        TemperatureUnit.KELVIN: 'K',
        TemperatureUnit.DEGREEFAHRENHEIT: '°F',
        TemperatureUnit.DEGREECELSIUS: '°C',
        TemperatureUnit.DEGREERANKINE: '°Ra',
        TemperatureUnit.DEGREEDELISLE: '°De',
        TemperatureUnit.DEGREENEWTON: '°N',
        TemperatureUnit.DEGREEREAUMUR: '°Ré',
        TemperatureUnit.DEGREEROEMER: '°Rø',
    }

    def __init__(self, value: float, unit: 'TemperatureUnit') -> None:
        self._value = value
        self._unit = unit

    def __str__(self):
        return "{value} {unit}".format(
            value=str(self._value),
            unit=Temperature.abbreviations[self._unit])

    def __repr__(self):
        return str(self)

    # Comparison operators
    def __eq__(self, other):
        return self._value == other.as_unit(self._unit)

    # Unary operators
    def __neg__(self):
        return Temperature(-self._value, self._unit)

    # Arithmetic operators
    def __add__(self, other):
        if type(other) is Temperature:
            return Temperature(self._value + other.as_unit(self._unit), self._unit)

        self._raise_type_error_for_undefined_operator(other, '+')

    def __sub__(self, other):
        if type(other) is Temperature:
            return Temperature(self._value - other.as_unit(self._unit), self._unit)

        self._raise_type_error_for_undefined_operator(other, '-')

    def __mul__(self, other):

        if type(other) in (float, int):
            result = Temperature(self._value * other, self._unit)
        else:
            self._raise_type_error_for_undefined_operator(other, '*')

        return result

    def __rmul__(self, other):

        if type(other) in (float, int, ):
            return self * other

        self._raise_type_error_for_undefined_operator(other, '*')

    def __truediv__(self, other):

        if type(other) is Temperature:
            result = (self._get_value_in_base_unit()
                    / other.as_unit(other.base_unit))
        elif type(other) in (float, int):
            result = Temperature(self._value / other, self._unit)
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
    def zero() -> 'Temperature':
        return Temperature(0, Temperature.base_unit)

    @property
    def unit(self) -> TemperatureUnit:
        return self._unit

    @property
    def value(self) -> float:
        return self._value

    def as_unit(self, unit: TemperatureUnit) -> float:
        if unit == self._unit:
            return self._value

        return self._get_value_as(unit)

    def to_unit(self, unit: TemperatureUnit) -> 'Temperature':
        converted_value = self._get_value_as(unit)

        return Temperature(converted_value, unit)

    # Generation shorthands
    @staticmethod
    def from_kelvin(value: float) -> 'Temperature':
        return Temperature(value, TemperatureUnit.KELVIN)

    @staticmethod
    def from_degrees_fahrenheit(value: float) -> 'Temperature':
        return Temperature(value, TemperatureUnit.DEGREEFAHRENHEIT)

    @staticmethod
    def from_degrees_celsius(value: float) -> 'Temperature':
        return Temperature(value, TemperatureUnit.DEGREECELSIUS)

    @staticmethod
    def from_degrees_rankine(value: float) -> 'Temperature':
        return Temperature(value, TemperatureUnit.DEGREERANKINE)

    @staticmethod
    def from_degrees_delisle(value: float) -> 'Temperature':
        return Temperature(value, TemperatureUnit.DEGREEDELISLE)

    @staticmethod
    def from_degrees_newton(value: float) -> 'Temperature':
        return Temperature(value, TemperatureUnit.DEGREENEWTON)

    @staticmethod
    def from_degrees_reaumur(value: float) -> 'Temperature':
        return Temperature(value, TemperatureUnit.DEGREEREAUMUR)

    @staticmethod
    def from_degrees_roemer(value: float) -> 'Temperature':
        return Temperature(value, TemperatureUnit.DEGREEROEMER)

    # Conversion shorthands
    @property
    def kelvin(self) -> float:
        return self.as_unit(TemperatureUnit.KELVIN)

    @property
    def degrees_fahrenheit(self) -> float:
        return self.as_unit(TemperatureUnit.DEGREEFAHRENHEIT)

    @property
    def degrees_celsius(self) -> float:
        return self.as_unit(TemperatureUnit.DEGREECELSIUS)

    @property
    def degrees_rankine(self) -> float:
        return self.as_unit(TemperatureUnit.DEGREERANKINE)

    @property
    def degrees_delisle(self) -> float:
        return self.as_unit(TemperatureUnit.DEGREEDELISLE)

    @property
    def degrees_newton(self) -> float:
        return self.as_unit(TemperatureUnit.DEGREENEWTON)

    @property
    def degrees_reaumur(self) -> float:
        return self.as_unit(TemperatureUnit.DEGREEREAUMUR)

    @property
    def degrees_roemer(self) -> float:
        return self.as_unit(TemperatureUnit.DEGREEROEMER)

    def _to_base_unit(self) -> 'Temperature':
        return self.to_unit(self.base_unit)

    def _get_value_in_base_unit(self) -> float:
        try:
            return self._value * Temperature.factors[self._unit] + Temperature.offsets[self._unit]
        except KeyError:
            raise NotImplementedError(
                'Can not convert {0} to base units.'.format(self._unit.name))

    def _get_value_as(self, unit: TemperatureUnit) -> float:
        base_unit_value = self._get_value_in_base_unit()

        try:
            return base_unit_value / Temperature.factors[unit]
        except KeyError:
            raise NotImplementedError(
                'Can not convert {0} to {1}.'.format(self._unit.name, unit))
