# Author: Lukas Halbritter <halbritl@informatik.uni-freiburg.de>
# Copyright 2020 - 2021
from ..units import AmountOfSubstanceUnit


class AmountOfSubstance:
    base_unit = AmountOfSubstanceUnit.MOLE
    factors = {
        AmountOfSubstanceUnit.MOLE: 1,
        AmountOfSubstanceUnit.CENTIMOLE: 1e-2,
        AmountOfSubstanceUnit.CENTIPOUNDMOLE: 453.59237e-2,
        AmountOfSubstanceUnit.DECIMOLE: 1e-1,
        AmountOfSubstanceUnit.DECIPOUNDMOLE: 453.59237e-1,
        AmountOfSubstanceUnit.KILOMOLE: 1e3,
        AmountOfSubstanceUnit.KILOPOUNDMOLE: 453.59237e3,
        AmountOfSubstanceUnit.MEGAMOLE: 1e6,
        AmountOfSubstanceUnit.MICROMOLE: 1e-6,
        AmountOfSubstanceUnit.MICROPOUNDMOLE: 453.59237e-6,
        AmountOfSubstanceUnit.MILLIMOLE: 1e-3,
        AmountOfSubstanceUnit.MILLIPOUNDMOLE: 453.59237e-3,
        AmountOfSubstanceUnit.NANOMOLE: 1e-9,
        AmountOfSubstanceUnit.NANOPOUNDMOLE: 453.59237e-9,
        AmountOfSubstanceUnit.POUNDMOLE: 453.59237,
    }
    abbreviations = {
        AmountOfSubstanceUnit.MOLE: 'mol',
        AmountOfSubstanceUnit.CENTIMOLE: 'cmol',
        AmountOfSubstanceUnit.CENTIPOUNDMOLE: 'clbmol',
        AmountOfSubstanceUnit.DECIMOLE: 'dmol',
        AmountOfSubstanceUnit.DECIPOUNDMOLE: 'dlbmol',
        AmountOfSubstanceUnit.KILOMOLE: 'kmol',
        AmountOfSubstanceUnit.KILOPOUNDMOLE: 'klbmol',
        AmountOfSubstanceUnit.MEGAMOLE: 'Mmol',
        AmountOfSubstanceUnit.MICROMOLE: 'µmol',
        AmountOfSubstanceUnit.MICROPOUNDMOLE: 'µlbmol',
        AmountOfSubstanceUnit.MILLIMOLE: 'mmol',
        AmountOfSubstanceUnit.MILLIPOUNDMOLE: 'mlbmol',
        AmountOfSubstanceUnit.NANOMOLE: 'nmol',
        AmountOfSubstanceUnit.NANOPOUNDMOLE: 'nlbmol',
        AmountOfSubstanceUnit.POUNDMOLE: 'lbmol',
    }

    def __init__(self, value: float, unit: 'AmountOfSubstanceUnit') -> None:
        self._value = value
        self._unit = unit

    def __str__(self):
        return "{value} {unit}".format(
            value=str(self._value),
            unit=AmountOfSubstance.abbreviations[self._unit])

    def __repr__(self):
        return str(self)

    # Comparison operators
    def __eq__(self, other):
        return self._value == other.as_unit(self._unit)

    # Unary operators
    def __neg__(self):
        return AmountOfSubstance(-self._value, self._unit)

    # Arithmetic operators
    def __add__(self, other):
        if type(other) is AmountOfSubstance:
            return AmountOfSubstance(self._value + other.as_unit(self._unit), self._unit)

        self._raise_type_error_for_undefined_operator(other, '+')

    def __sub__(self, other):
        if type(other) is AmountOfSubstance:
            return AmountOfSubstance(self._value - other.as_unit(self._unit), self._unit)

        self._raise_type_error_for_undefined_operator(other, '-')

    def __mul__(self, other):

        if type(other) in (float, int):
            result = AmountOfSubstance(self._value * other, self._unit)
        else:
            self._raise_type_error_for_undefined_operator(other, '*')

        return result

    def __rmul__(self, other):

        if type(other) in (float, int, ):
            return self * other

        self._raise_type_error_for_undefined_operator(other, '*')

    def __truediv__(self, other):

        if type(other) is AmountOfSubstance:
            result = (self._get_value_in_base_unit()
                    / other.as_unit(other.base_unit))
        elif type(other) in (float, int):
            result = AmountOfSubstance(self._value / other, self._unit)
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
    def zero() -> 'AmountOfSubstance':
        return AmountOfSubstance(0, AmountOfSubstance.base_unit)

    @property
    def unit(self) -> AmountOfSubstanceUnit:
        return self._unit

    @property
    def value(self) -> float:
        return self._value

    def as_unit(self, unit: AmountOfSubstanceUnit) -> float:
        if unit == self._unit:
            return self._value

        return self._get_value_as(unit)

    def to_unit(self, unit: AmountOfSubstanceUnit) -> 'AmountOfSubstance':
        converted_value = self._get_value_as(unit)

        return AmountOfSubstance(converted_value, unit)

    # Generation shorthands
    @staticmethod
    def from_moles(value: float) -> 'AmountOfSubstance':
        return AmountOfSubstance(value, AmountOfSubstanceUnit.MOLE)

    @staticmethod
    def from_centimoles(value: float) -> 'AmountOfSubstance':
        return AmountOfSubstance(value, AmountOfSubstanceUnit.CENTIMOLE)

    @staticmethod
    def from_centipound_moles(value: float) -> 'AmountOfSubstance':
        return AmountOfSubstance(value, AmountOfSubstanceUnit.CENTIPOUNDMOLE)

    @staticmethod
    def from_decimoles(value: float) -> 'AmountOfSubstance':
        return AmountOfSubstance(value, AmountOfSubstanceUnit.DECIMOLE)

    @staticmethod
    def from_decipound_moles(value: float) -> 'AmountOfSubstance':
        return AmountOfSubstance(value, AmountOfSubstanceUnit.DECIPOUNDMOLE)

    @staticmethod
    def from_kilomoles(value: float) -> 'AmountOfSubstance':
        return AmountOfSubstance(value, AmountOfSubstanceUnit.KILOMOLE)

    @staticmethod
    def from_kilopound_moles(value: float) -> 'AmountOfSubstance':
        return AmountOfSubstance(value, AmountOfSubstanceUnit.KILOPOUNDMOLE)

    @staticmethod
    def from_megamoles(value: float) -> 'AmountOfSubstance':
        return AmountOfSubstance(value, AmountOfSubstanceUnit.MEGAMOLE)

    @staticmethod
    def from_micromoles(value: float) -> 'AmountOfSubstance':
        return AmountOfSubstance(value, AmountOfSubstanceUnit.MICROMOLE)

    @staticmethod
    def from_micropound_moles(value: float) -> 'AmountOfSubstance':
        return AmountOfSubstance(value, AmountOfSubstanceUnit.MICROPOUNDMOLE)

    @staticmethod
    def from_millimoles(value: float) -> 'AmountOfSubstance':
        return AmountOfSubstance(value, AmountOfSubstanceUnit.MILLIMOLE)

    @staticmethod
    def from_millipound_moles(value: float) -> 'AmountOfSubstance':
        return AmountOfSubstance(value, AmountOfSubstanceUnit.MILLIPOUNDMOLE)

    @staticmethod
    def from_nanomoles(value: float) -> 'AmountOfSubstance':
        return AmountOfSubstance(value, AmountOfSubstanceUnit.NANOMOLE)

    @staticmethod
    def from_nanopound_moles(value: float) -> 'AmountOfSubstance':
        return AmountOfSubstance(value, AmountOfSubstanceUnit.NANOPOUNDMOLE)

    @staticmethod
    def from_pound_moles(value: float) -> 'AmountOfSubstance':
        return AmountOfSubstance(value, AmountOfSubstanceUnit.POUNDMOLE)

    # Conversion shorthands
    @property
    def moles(self) -> float:
        return self.as_unit(AmountOfSubstanceUnit.MOLE)

    @property
    def centimoles(self) -> float:
        return self.as_unit(AmountOfSubstanceUnit.CENTIMOLE)

    @property
    def centipound_moles(self) -> float:
        return self.as_unit(AmountOfSubstanceUnit.CENTIPOUNDMOLE)

    @property
    def decimoles(self) -> float:
        return self.as_unit(AmountOfSubstanceUnit.DECIMOLE)

    @property
    def decipound_moles(self) -> float:
        return self.as_unit(AmountOfSubstanceUnit.DECIPOUNDMOLE)

    @property
    def kilomoles(self) -> float:
        return self.as_unit(AmountOfSubstanceUnit.KILOMOLE)

    @property
    def kilopound_moles(self) -> float:
        return self.as_unit(AmountOfSubstanceUnit.KILOPOUNDMOLE)

    @property
    def megamoles(self) -> float:
        return self.as_unit(AmountOfSubstanceUnit.MEGAMOLE)

    @property
    def micromoles(self) -> float:
        return self.as_unit(AmountOfSubstanceUnit.MICROMOLE)

    @property
    def micropound_moles(self) -> float:
        return self.as_unit(AmountOfSubstanceUnit.MICROPOUNDMOLE)

    @property
    def millimoles(self) -> float:
        return self.as_unit(AmountOfSubstanceUnit.MILLIMOLE)

    @property
    def millipound_moles(self) -> float:
        return self.as_unit(AmountOfSubstanceUnit.MILLIPOUNDMOLE)

    @property
    def nanomoles(self) -> float:
        return self.as_unit(AmountOfSubstanceUnit.NANOMOLE)

    @property
    def nanopound_moles(self) -> float:
        return self.as_unit(AmountOfSubstanceUnit.NANOPOUNDMOLE)

    @property
    def pound_moles(self) -> float:
        return self.as_unit(AmountOfSubstanceUnit.POUNDMOLE)

    def _to_base_unit(self) -> 'AmountOfSubstance':
        return self.to_unit(self.base_unit)

    def _get_value_in_base_unit(self) -> float:
        try:
            return self._value * AmountOfSubstance.factors[self._unit]
        except KeyError:
            raise NotImplementedError(
                'Can not convert {0} to base units.'.format(self._unit.name))

    def _get_value_as(self, unit: AmountOfSubstanceUnit) -> float:
        base_unit_value = self._get_value_in_base_unit()

        try:
            return base_unit_value / AmountOfSubstance.factors[unit]
        except KeyError:
            raise NotImplementedError(
                'Can not convert {0} to {1}.'.format(self._unit.name, unit))
