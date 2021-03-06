# AllYourUnitAreBelongToUs
![version](https://img.shields.io/github/license/MCHalbi/AllYourUnitAreBelongToUs)
![version](https://img.shields.io/pypi/v/ayuabtu)
![version](https://img.shields.io/github/workflow/status/MCHalbi/AllYourUnitAreBelongToUs/Codestyle%20and%20unittests?label=tests)
![version](https://img.shields.io/codecov/c/github/MCHalbi/AllYourUnitAreBelongToUs)

## Installation
```
pip install ayuabtu
```

## Usage
### Creating quantities
Create quantities with a given unit:
```
>>> from ayuabtu.quantities import Length
>>> from ayuabtu.units import LengthUnit
>>> Length(2, LengthUnit.METER)
2 m
```
Or you can use the unit specific factory methods:
```
>>> from ayuabtu.quantities import Length
>>> Length.from_meters(2)
2 m
```
You can also access only the value with
```
>>> from ayuabtu.quantities import Length
>>> Length.from_meters(2).value
2
```

### Converting units
You can convert a quantity to a quantity with another unit
```
>>> from ayuabtu.quantities import Length
>>> from ayuabtu.units import LengthUnit
>>> distance_metric = Length.from_meters(2)
>>> distance_metric.to_unit(LengthUnit.FOOT)
6.561679790026246 ft
```
If you just need the numeric value of the quantity, but expressed in another
unit, use
```
>>> from ayuabtu.quantities import Length
>>> from ayuabtu.units import LengthUnit
>>> distance_metric = Length.from_meters(2)
>>> distance_metric.as_unit(LengthUnit.FOOT)
6.561679790026246
```
For this common usecase, there are also shorthand methods:
```
>>> from ayuabtu.quantities import Length
>>> distance_metric = Length.from_meters(2)
>>> distance_metric.feet()
6.561679790026246
```

### Quantity arithmetics
Coming soon ...

## Custom units
Coming soon ...
