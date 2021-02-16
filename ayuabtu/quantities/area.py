# Author: Lukas Halbritter <halbritl@informatik.uni-freiburg.de>
# Copyright 2020 - 2021
from ..units import AreaUnit


class Area:
    base_unit = AreaUnit.SQUAREMETER
    factors = {
        AreaUnit.SQUAREKILOMETER: 1e6,
        AreaUnit.HECTARE: 1e4,
        AreaUnit.SQUAREMETER: 1,
        AreaUnit.SQUAREDECIMETER: 1e-2,
        AreaUnit.SQUARECENTIMETER: 1e-4,
        AreaUnit.SQUAREMILLIMETER: 1e-6,
        AreaUnit.SQUAREMICROMETER: 1e-12,
        AreaUnit.SQUAREINCH: 6.4516e-4,
        AreaUnit.SQUAREFOOT: 9.2903e-2,
        AreaUnit.SQUAREYARD: 8.36127e-1,
        AreaUnit.SQUAREMILE: 2.59e6,
        AreaUnit.ACRE: 4046.85642,
    }
    abbreviations = {
        AreaUnit.SQUAREKILOMETER: 'km²',
        AreaUnit.HECTARE: 'ha',
        AreaUnit.SQUAREMETER: 'm²',
        AreaUnit.SQUAREDECIMETER: 'dm²',
        AreaUnit.SQUARECENTIMETER: 'cm²',
        AreaUnit.SQUAREMILLIMETER: 'mm²',
        AreaUnit.SQUAREMICROMETER: 'μm²',
        AreaUnit.SQUAREINCH: 'in²',
        AreaUnit.SQUAREFOOT: 'ft²',
        AreaUnit.SQUAREYARD: 'yd²',
        AreaUnit.SQUAREMILE: 'mi²',
        AreaUnit.ACRE: 'ac',
    }

    def __init__(self, value: float, unit: 'AreaUnit') -> None:
        self._value = value
        self._unit = unit

    def __str__(self):
        return "{value} {unit}".format(
            value=str(self._value),
            unit=Area.abbreviations[self._unit])

    def __repr__(self):
        return str(self)

    # Comparison operators
    def __eq__(self, other):
        return self._value == other.as_unit(self._unit)

    # Unary operators
    def __neg__(self):
        return Area(-self._value, self._unit)

    # Arithmetic operators
    def __add__(self, other):
        if type(other) is Area:
            return Area(self._value + other.as_unit(self._unit), self._unit)

        self._raise_type_error_for_undefined_operator(other, '+')

    def __sub__(self, other):
        if type(other) is Area:
            return Area(self._value - other.as_unit(self._unit), self._unit)

        self._raise_type_error_for_undefined_operator(other, '-')

    def __mul__(self, other):
        from .length import Length
        from .volume import Volume

        if type(other) in (float, int):
            result = Area(self._value * other, self._unit)
        elif type(other) is Length:
            result = Volume(
                self.as_unit(self.base_unit) * other.as_unit(other.base_unit),
                Volume.base_unit)
        else:
            self._raise_type_error_for_undefined_operator(other, '*')

        return result

    def __rmul__(self, other):
        from .length import Length
        from .volume import Volume

        if type(other) in (float, int, Length):
            return self * other

        self._raise_type_error_for_undefined_operator(other, '*')

    def __truediv__(self, other):
        from .length import Length

        if type(other) is Area:
            result = (self._get_value_in_base_unit()
                    / other.as_unit(other.base_unit))
        elif type(other) in (float, int):
            result = Area(self._value / other, self._unit)
        elif type(other) is Length:
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
    def zero() -> 'Area':
        return Area(0, Area.base_unit)

    @property
    def unit(self) -> AreaUnit:
        return self._unit

    @property
    def value(self) -> float:
        return self._value

    def as_unit(self, unit: AreaUnit) -> float:
        if unit == self._unit:
            return self._value

        return self._get_value_as(unit)

    def to_unit(self, unit: AreaUnit) -> 'Area':
        converted_value = self._get_value_as(unit)

        return Area(converted_value, unit)

    # Generation shorthands
    @staticmethod
    def from_square_kilometers(value: float) -> 'Area':
        return Area(value, AreaUnit.SQUAREKILOMETER)

    @staticmethod
    def from_hectares(value: float) -> 'Area':
        return Area(value, AreaUnit.HECTARE)

    @staticmethod
    def from_square_meters(value: float) -> 'Area':
        return Area(value, AreaUnit.SQUAREMETER)

    @staticmethod
    def from_square_decimeters(value: float) -> 'Area':
        return Area(value, AreaUnit.SQUAREDECIMETER)

    @staticmethod
    def from_square_centimeters(value: float) -> 'Area':
        return Area(value, AreaUnit.SQUARECENTIMETER)

    @staticmethod
    def from_square_millimeters(value: float) -> 'Area':
        return Area(value, AreaUnit.SQUAREMILLIMETER)

    @staticmethod
    def from_square_micrometers(value: float) -> 'Area':
        return Area(value, AreaUnit.SQUAREMICROMETER)

    @staticmethod
    def from_square_inches(value: float) -> 'Area':
        return Area(value, AreaUnit.SQUAREINCH)

    @staticmethod
    def from_square_feet(value: float) -> 'Area':
        return Area(value, AreaUnit.SQUAREFOOT)

    @staticmethod
    def from_square_yards(value: float) -> 'Area':
        return Area(value, AreaUnit.SQUAREYARD)

    @staticmethod
    def from_square_miles(value: float) -> 'Area':
        return Area(value, AreaUnit.SQUAREMILE)

    @staticmethod
    def from_acres(value: float) -> 'Area':
        return Area(value, AreaUnit.ACRE)

    # Conversion shorthands
    @property
    def square_kilometers(self) -> float:
        return self.as_unit(AreaUnit.SQUAREKILOMETER)

    @property
    def hectares(self) -> float:
        return self.as_unit(AreaUnit.HECTARE)

    @property
    def square_meters(self) -> float:
        return self.as_unit(AreaUnit.SQUAREMETER)

    @property
    def square_decimeters(self) -> float:
        return self.as_unit(AreaUnit.SQUAREDECIMETER)

    @property
    def square_centimeters(self) -> float:
        return self.as_unit(AreaUnit.SQUARECENTIMETER)

    @property
    def square_millimeters(self) -> float:
        return self.as_unit(AreaUnit.SQUAREMILLIMETER)

    @property
    def square_micrometers(self) -> float:
        return self.as_unit(AreaUnit.SQUAREMICROMETER)

    @property
    def square_inches(self) -> float:
        return self.as_unit(AreaUnit.SQUAREINCH)

    @property
    def square_feet(self) -> float:
        return self.as_unit(AreaUnit.SQUAREFOOT)

    @property
    def square_yards(self) -> float:
        return self.as_unit(AreaUnit.SQUAREYARD)

    @property
    def square_miles(self) -> float:
        return self.as_unit(AreaUnit.SQUAREMILE)

    @property
    def acres(self) -> float:
        return self.as_unit(AreaUnit.ACRE)

    def _to_base_unit(self) -> 'Area':
        return self.to_unit(self.base_unit)

    def _get_value_in_base_unit(self) -> float:
        try:
            return self._value * Area.factors[self._unit]
        except KeyError:
            raise NotImplementedError(
                'Can not convert {0} to base units.'.format(self._unit.name))

    def _get_value_as(self, unit: AreaUnit) -> float:
        base_unit_value = self._get_value_in_base_unit()

        try:
            return base_unit_value / Area.factors[unit]
        except KeyError:
            raise NotImplementedError(
                'Can not convert {0} to {1}.'.format(self._unit.name, unit))
