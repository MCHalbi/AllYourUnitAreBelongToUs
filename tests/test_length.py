# Author: Lukas Halbritter <halbritl@informatik.uni-freiburg.de>
# Copyright 2020
# pylint: disable=missing-docstring
import unittest
from pythonunits.quantities import Length
from pythonunits.units import LengthUnit


class LengthTests(unittest.TestCase):
    def setUp(self):
        self._zero = Length.zero()
        self._kilometers = Length(1, LengthUnit.KILOMETER)
        self._hectometers = Length(1, LengthUnit.HECTOMETER)
        self._decameters = Length(1, LengthUnit.DECAMETER)
        self._meters = Length(1, LengthUnit.METER)
        self._decimeters = Length(1, LengthUnit.DECIMETER)
        self._centimeters = Length(1, LengthUnit.CENTIMETER)
        self._millimeters = Length(1, LengthUnit.MILLIMETER)
        self._micrometers = Length(1, LengthUnit.MICROMETER)
        self._nanometers = Length(1, LengthUnit.NANOMETER)

    def test_base_unit_is_meter(self):
        self.assertEqual(LengthUnit.METER, Length.base_unit)

    def test_zero_object_has_zero_value(self):
        self.assertAlmostEqual(0, self._zero.as_unit(LengthUnit.METER))

    def test_zero_object_has_base_unit(self):
        self.assertEqual(LengthUnit.METER, self._zero.unit)

    def test_converted_to_base_unit_length_has_base_unit(self):
        self.assertEqual(LengthUnit.METER, self._kilometers.to_base_unit().unit)

    def test_kilometer_converted_to_base_unit_has_correct_value(self):
        self.assertEqual(1e3, self._kilometers.to_base_unit().value)

    def test_hectometer_converted_to_base_unit_has_correct_value(self):
        self.assertEqual(1e2, self._hectometers.to_base_unit().value)
