# Author: Lukas Halbritter <halbritl@informatik.uni-freiburg.de>
# Copyright 2021
import json
import os
from case_conversion import snakecase, pascalcase
from pandas.io.json import json_normalize
from typing import List


class QuantityManager:
    def __init__(self, source_dir: str) -> None:
        self._source_dir = source_dir
        self._available_quantities = self._init_available_quantity_list()
        self._loaded_quantity = {}
        self._unsafed = False

    @property
    def source_dir(self) -> str:
        return self._source_dir

    @property
    def quantity_loaded(self) -> bool:
        return bool(self._loaded_quantity)

    @property
    def current_quantity_name(self) -> str:
        return self._loaded_quantity.get('name', 'No quantity loaded.')

    @property
    def has_pending_changes(self) -> bool:
        return self._unsafed

    @property
    def available_quantities(self) -> List[str]:
        return self._available_quantities

    def is_quantity_available(self, quantity_name: str) -> bool:
        return quantity_name in self._available_quantities

    def set_base_unit(self, unit_name: str) -> None:
        self._loaded_quantity['baseunit'] = pascalcase(unit_name)
        self._unsafed = True

    def new_quantity(self, quantity_name: str) -> None:
        pascal_quantity_name = pascalcase(quantity_name)

        self._loaded_quantity = {
            'name': pascal_quantity_name,
            'baseunit': None,
            'units': [],
            'operators': {'mul': [], 'div': []},
            }
        self._available_quantities.append(pascal_quantity_name + ' (new)*')
        self._unsafed = True

    def add_unit(
            self,
            unit_name: str,
            unit_factor: str,
            unit_abbreviation: str) -> None:
        new_unit = {
            'name': pascalcase(unit_name),
            'factor': unit_factor,
            'abbreviation': unit_abbreviation,
            }

        self._loaded_quantity['units'].append(new_unit)
        self._add_unsafed_star()
        self._unsafed = True

    def add_operator(
            self,
            op_type: str,
            other_type: str,
            result_type: str) -> None:
        new_op = {'other': other_type, 'result': result_type}

        self._loaded_quantity['operators'][op_type].append(new_op)
        self._add_unsafed_star()
        self._unsafed = True

    def remove_unit(self, unit_index: int) -> None:
        del self._loaded_quantity['units'][unit_index]
        self._add_unsafed_star()
        self._unsafed = True

    def remove_quantity(self, quantity_name: str) -> None:
        filename = os.path.join(
            self._source_dir,
            snakecase(quantity_name) + '.json')

        try:
            os.remove(filename)
        except FileNotFoundError:
            print('There is no quantity definition file for \'{0}\'.'
                  .format(pascalcase(quantity_name)))
            return

        if self.current_quantity_name == pascalcase(quantity_name):
            self._add_unsafed_star()
            self._unsafed = True
        else:
            self._available_quantities.remove(pascalcase(quantity_name))

    def load(self, quantity_name: str) -> None:
        filename = os.path.join(
            self._source_dir,
            snakecase(quantity_name) + '.json')

        try:
            with open(filename) as quantity_file:
                self._loaded_quantity = json.load(quantity_file)
        except FileNotFoundError:
            print('There is no quantity definition file for \'{0}\'.'
                  .format(pascalcase(quantity_name)))
            return

        self._unsafed = False

    def store(self) -> None:
        filename = os.path.join(
            self._source_dir,
            snakecase(self.current_quantity_name) + '.json')

        with open(filename, 'w') as quantity_file:
            json.dump(self._loaded_quantity, quantity_file, indent=2)

        self._available_quantities = self._init_available_quantity_list()
        self._unsafed = False

    def list_units(self, with_index: bool = False) -> None:
        if self._loaded_quantity:
            print('Base unit: ' + self._loaded_quantity['baseunit'])
            print(
                json_normalize(self._loaded_quantity['units'])
                .sort_values(by='name')
                .to_string(
                    index=with_index,
                    columns=['name', 'abbreviation', 'factor']))
        else:
            print('No quantity loaded.')

    def list_operators(self) -> None:
        if self._loaded_quantity:
            for op in self._loaded_quantity['operators'].get('mul', {}):
                print(
                    '*: {0} x {1} -> {2}'
                    .format(
                        self._loaded_quantity['name'],
                        op['other'],
                        op['result']))
            for op in self._loaded_quantity['operators'].get('div', {}):
                print(
                    '/: {0} x {1} -> {2}'
                    .format(
                        self._loaded_quantity['name'],
                        op['other'],
                        op['result']))
        else:
            print('No quantity loaded.')

    def list_quantities(self) -> None:
        for quantity in self._available_quantities:
            print(quantity)

    def unit_name_by_index(self, index: int) -> str:
        return self._loaded_quantity['units'][index]['name']

    def _init_available_quantity_list(self) -> List:
        available_quantities = []

        for filename_with_ext in sorted(os.listdir(self._source_dir)):
            (filename, ext) = os.path.splitext(filename_with_ext)
            if ext == '.json':
                available_quantities.append(pascalcase(filename))

        return available_quantities

    def _add_unsafed_star(self) -> None:
        self._available_quantities = [
            quantity + '*'
            if (quantity == self.current_quantity_name
                and not self.current_quantity_name.endswith('*'))
            else quantity
            for quantity in self._available_quantities]

    def _base_value_abbreviation(self) -> str:
        return next(
            (unit['abbreviation']
             for unit in self._loaded_quantity['units']
             if unit['name'] == self._loaded_quantity['baseunit']),
            None)
