# AllYourUnitAreBelongToUs
![version](https://img.shields.io/github/license/MCHalbi/AllYourUnitAreBelongToUs)
![version](https://img.shields.io/pypi/v/ayuabtu)
![version](https://img.shields.io/github/workflow/status/MCHalbi/AllYourUnitAreBelongToUs/Codestyle%20and%20unittests?label=tests)
![version](https://img.shields.io/codecov/c/github/MCHalbi/AllYourUnitAreBelongToUs)

A Python package with everything you will ever want and need when dealing with
units.

AYUABTU currently contains 9 quantities with 115
different units. You can also make use of the 0 predefined
constants.<br />
You need you own, fancy units? Define them yourself! With the Quantity
Manager tool you can modify AYUABTU to fit your needs without fiddling with any
config files.<br />
No more implicit units, no more struggling with unit conversion.

And the best thing is: All that comes out of the box, with
AYUABTU, with ease!

## Installation
```
pip install ayuabtu
```

## Prerequisites
AYUABTU itself does not depend on any other package. However, if you wish to add
your own quantities and units, the [Quantity Manager](#the-quantity-manager-qm)
and [Package Generator](#re-generating-the-ayuabtu-package) depend on some
thid-party python packages. The dependencies of the Quantity Manager and its
shell are:

- [case-conversion](https://github.com/AlejandroFrias/case-conversion)
- [pandas](https://pypi.org/project/pandas/)

To run the Package Generator, you will need the following packages:

- [Jinja2](https://pypi.org/project/Jinja2/)
- [case-conversion](https://github.com/AlejandroFrias/case-conversion)


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
### The Quantity Manager (QM)
The code of the AYUABTU package is generated from a set of quantity definition
files (QDF). A QDF is just a JSON file containing the definitions of all units
and operators of a certain quantity. You can find the quantity definition files in
[package_generation/quantity_definitions/](package_generation/quantity_definitions/).
To add new units or even quantities, you are recommended to ues the Quantity
Manger:
```
$ cd package_generation/quantity_manager
$ python qm_start.py
```

You should see a nice little shell which allows you to interact with the
Quantity Manager. You can add and remove units, quantities and operators from
this shell. Let's start with listing all available quantities:
```
QM> ls quantities
AmountOfSubstance
ElectricCurrent
Length
LuminousIntensity
Mass
Temperature
Time
```

We now want to add a new quantity for Area. We do that by typing
```
QM> add quantity
```

The QM now asks for a name of the quantity and the name and abbreviation of the
base unit of this quantity.
```
Enter the name of the new quantity: Area
Enter the name of the base unit of 'Area': SquareMeter
Enter the abbreviation for 'SquareMeter': m²
```

When we now execute `ls quantities` again, we can see the entry `Area (new)*`.
Our new quantity is not yet stored in a file. Let's store our Area quantity:

```
QM> store
```

Running `ls quantities` again now shows us `Area` alongside with the other
quantities. The quantity has been stored as JSON file in the
quantity_definitions folder.

To add another unit for Area, we type:
```
QM> add unit
```

Once again, we are asked to enter the definition of the unit, now with the
factor of the unit which allows us to convert this unit to the base unit:
```
Enter the unit name: SquareCentimeter
Enter the unit abbreviation: cm²
Enter the unit factor: 1e-4
```

Running the list command shows us the two units of our Area quantity:
```
QM> ls units
Base unit: SquareMeter
             name abbreviation factor
 SquareCentimeter          cm²   1e-4
      SquareMeter           m²      1

```

To be able to use the quantity for arithmetic operations, we have to add
operators. Since Area divided by Length is Length, we add a division operator:
```
QM> add op
Enter the operation type (mul/div): div
Enter the quantity type of the second operand: Length
Enter the quantity type of the result: Length
```

When listing the operators of our Area quantity, we now see the newly added
division operator:
```
QM> ls op
/: Area x Length -> Length
```

### Re-generating the AYUABTU package