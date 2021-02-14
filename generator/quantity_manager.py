# Author: Lukas Halbritter <halbritl@informatik.uni-freiburg.de>
# Copyright 2021
import json
import os
from case_conversion import snakecase, pascalcase
from cmd import Cmd
from pandas.io.json import json_normalize


class QuantityManager:
    def __init__(self, source_dir: str) -> None:
        self._source_dir = source_dir
        self._loaded_quantity = {}
        self._unsafed = False

    def new(self, quantity_name: str) -> None:
        self._loaded_quantity = {
            'name': pascalcase(quantity_name),
            'baseunit': None,
            'units': [],
            'operators': {'mul': [], 'div': []},
            }
        self._unsafed = True

    @property
    def has_pending_changes(self):
        return self._unsafed

    @property
    def quantity_loaded(self) -> bool:
        return bool(self._loaded_quantity)

    @property
    def current_quantity(self) -> str:
        return self._loaded_quantity.get('name', 'No quantity loaded.')

    @property
    def source_dir(self) -> str:
        return self._source_dir

    def set_base_unit(self, unit_name: str) -> None:
        self._loaded_quantity['baseunit'] = pascalcase(unit_name)
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
        self._unsafed = True

    def load(self, quantity_name: str) -> None:
        filename = os.path.join(
            self._source_dir,
            snakecase(quantity_name) + '.json')
        with open(filename) as quantity_file:
            self._loaded_quantity = json.load(quantity_file)

    def store(self) -> None:
        filename = os.path.join(
            self._source_dir,
            snakecase(self._loaded_quantity['name']) + '.json')

        with open(filename, 'w') as quantity_file:
            json.dump(self._loaded_quantity, quantity_file)
        self._unsafed = False

    def list_units(self) -> None:
        if self._loaded_quantity:
            print(
                json_normalize(self._loaded_quantity['units'])
                .sort_values(by='name')
                .to_string(
                    index=False,
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
        for filename_with_ext in sorted(os.listdir(self._source_dir)):
            (filename, ext) = os.path.splitext(filename_with_ext)
            if ext == '.json':
                print(pascalcase(filename))

    def _base_value_abbreviation(self) -> str:
        return next((unit['abbreviation']
              for unit in self._loaded_quantity['units']
              if unit['name'] == self._loaded_quantity['baseunit']),
             None)


class QMShell(Cmd):
    intro = ("=== Welcome to the Quantity Manager! ===\n"
             "Edit quantity source files for AYUABTU with ease.")
    prompt = 'QM> '

    def preloop(self):
        self._quantity_manager = QuantityManager('./quantity_definitions/')

    def do_ls(self, args):
        if (args == 'units'):
            self._quantity_manager.list_units()
        elif (args == 'quantities'):
            self._quantity_manager.list_quantities()
        elif (args == 'operators'):
            self._quantity_manager.list_operators()
        else:
            print('*** unknown argument \'{0}\''.format(args))

    def do_current(self, args):
        print(self._quantity_manager.current_quantity)

    def complete_ls(self, text, line, begidx, endidx):
        ls_args = ['units', 'quantities', 'operators']
        if text:
            return [arg for arg in ls_args if arg.startswith(text)]

        return ls_args

    def do_load(self, arg):
        'Load a quantity from a quantity definition file.'
        if self._quantity_manager.has_pending_changes:
            exit_choice = input(
                'There are unsafed changes. Loading a quantity without storing '
                + 'the current one will overwrite any unsafed changes. '
                + 'Proceed anyway? (y/N):')

            if exit_choice not in ['y', 'Y', 'yes', 'Yes']:
                return

        self._quantity_manager.load(arg)

    def do_new(self, args):
        'Create a new quantity.'
        if self._quantity_manager.has_pending_changes:
            exit_choice = input(
                'There are unsafed changes. Creating a new quantity without '
                + 'storing the current one will overwrite any unsafed changes. '
                + 'Proceed anyway? (y/N):')

            if exit_choice not in ['y', 'Y', 'yes', 'Yes']:
                return

        quantity_name = input('Enter the name of the new quantity: ')

        self._quantity_manager.new(quantity_name)

        base_unit = input(
            'Enter the name of the base unit of \'{0}\': '
            .format(quantity_name))

        self._quantity_manager.set_base_unit(base_unit)

        abbreviation = input(
            'Enter the abbreviation for \'{0}\': '
            .format(base_unit))

        self._quantity_manager.add_unit(base_unit, '1', abbreviation)

    def do_add(self, args):
        'Add a new unit to the current quantity.'
        unit_name = input('Enter the unit name: ')
        unit_abbreviation = input('Enter the unit abbreviation: ')
        unit_factor = input('Enter the unit factor: ')

        self._quantity_manager.add_unit(
            unit_name, unit_factor, unit_abbreviation)

    def do_store(self, args):
        'Store the current quantity.'
        filename = snakecase(self._quantity_manager.current_quantity)
        full_filename = os.path.join(
            self._quantity_manager.source_dir, filename + '.json')

        if os.path.isfile(full_filename):
            overwrite = input(
                'The quantity definition file for \'{0}\' already exists in '
                .format(self._quantity_manager.current_quantity)
                + '\'{0}\'. Do you want to overwrite it? (y/N): '
                .format(self._quantity_manager.source_dir))
            if not overwrite:
                return

        self._quantity_manager.store()

    def do_exit(self, args):
        'Exit the QuantityManager.'
        if self._quantity_manager.has_pending_changes:
            exit_choice = input(
                'There are unsafed changes. Do you really want to exit? (y/N):')

            if exit_choice not in ['y', 'Y', 'yes', 'Yes']:
                return

        return True

    def do_EOF(self, arg):
        return self.do_exit(arg)


if __name__ == '__main__':
    QMShell().cmdloop()
