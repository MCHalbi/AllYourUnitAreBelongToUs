# Author: Lukas Halbritter <halbritl@informatik.uni-freiburg.de>
# Copyright 2021
import os
from case_conversion import snakecase, pascalcase
from cmd import Cmd
from quantity_manager import QuantityManager

class QMShell(Cmd):
    intro = ("=== Welcome to the Quantity Manager! ===\n"
             "Edit quantity source files for AYUABTU with ease.")
    prompt = 'QM> '

    def __init__(self, definition_file_directory: str) -> None:
        self._quantity_manager = QuantityManager(definition_file_directory)
        super().__init__()

    def do_list(self, args):
        ('Lists available quantites, units and operators:\n\n'
         '    list units           Lists all units of the currently loaded quantity.\n'
         '    list quantities, qt  Lists all available quantities.\n'
         '    list operators, op   Lists all operators of the currently loaded quantity.\n')
        if (args == 'units'):
            self._quantity_manager.list_units()
        elif args in ('quantities', 'qt'):
            self._quantity_manager.list_quantities()
        elif args in ('operators', 'op'):
            self._quantity_manager.list_operators()
        else:
            print('*** unknown argument \'{0}\''.format(args))

    def do_ls(self, args):
        'Alias for list.'
        self.do_list(args)

    def complete_list(self, text, line, begidx, endidx):
        ls_args = ['units', 'quantities', 'operators']
        if text:
            return [arg for arg in ls_args if arg.startswith(text)]

        return ls_args

    def complete_ls(self, text, line, begidx, endidx):
        return self.complete_list(text, line, begidx, endidx)

    def do_current(self, args):
        'Print the name of the currently loaded quantity.'
        print(self._quantity_manager.current_quantity_name)

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

    def complete_load(self, text, line, begidx, endidx):
        quantities = self._quantity_manager.available_quantities
        if text:
            return [qt for qt in quantities if qt.startswith(text)]

        return quantities

    def do_add(self, args):
        ('Add a new unit, operator or quantity:\n\n'
         '    add quantity, qt  Adds a new quantity.\n'
         '    add unit          Adds a new unit to the currently loaded quantity.\n'
         '    add operator, op  Adds a new operators to the currently loaded quantity.\n')
        if args == 'unit':
            self._add_unit()
        elif args in ('operator', 'op'):
            self._add_operator()
        elif args in ('quantity', 'qt'):
            self._add_quantity()
        else:
            print('*** unknown argument \'{0}\''.format(args))

    def complete_add(self, text, line, begidx, endidx):
        add_args = ['unit', 'quantity', 'operator']
        if text:
            return [arg for arg in add_args if arg.startswith(text)]

        return add_args

    def do_rm(self, args):
        ('Removes a unit, operator or quantity:\n\n'
         '    rm quantity, qt  Removes quantity.\n'
         '    rm unit          Removes unit from the currently loaded quantity.\n'
         '    rm operator, op  Removes operators from the currently loaded quantity.\n')
        if args == 'unit':
            self._remove_unit()
        elif args in ('operator', 'op'):
            self._remove_operator()
        elif args in ('quantity', 'qt'):
            self._remove_quantity()
        else:
            print('*** unknown argument \'{0}\''.format(args))

    def complete_rm(self, text, line, begidx, endidx):
        rm_args = ['unit', 'quantity', 'operator']
        if text:
            return [arg for arg in rm_args if arg.startswith(text)]

        return rm_args

    def do_store(self, *args):
        'Store the current quantity.'
        filename = snakecase(self._quantity_manager.current_quantity_name)
        full_filename = os.path.join(
            self._quantity_manager.source_dir, filename + '.json')

        if '-f' not in args and os.path.isfile(full_filename):
            overwrite_info = (
                'The quantity definition file for \'{0}\' already exists in '
                + '\'{1}\'. Do you want to overwrite it? (y/N): ')
            overwrite = input(
                overwrite_info
                .format(self._quantity_manager.current_quantity_name,
                        self._quantity_manager.source_dir))
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
        'Alias for exit.'
        return self.do_exit(arg)

    def _add_quantity(self) -> None:
        if self._quantity_manager.has_pending_changes:
            exit_choice = input(
                'There are unsafed changes. Creating a new quantity without '
                + 'storing the current one will overwrite any unsafed changes. '
                + 'Proceed anyway? (y/N):')

            if exit_choice not in ['y', 'Y', 'yes', 'Yes']:
                return

        quantity_name = input('Enter the name of the new quantity: ')

        if self._quantity_manager.is_quantity_available(quantity_name):
            overwrite_info = (
                'There is already a quantity definition file for the quantity '
                + '\'{0}\'. When you create a new quantity with a name that '
                'exists, the existing quantity definition file will be '
                'overwritten when storing the new quantity. You may use \'load '
                '{0}\' to load the existing quantity definition file. Do you '
                + 'want to proceed anyway? (y/N): ')
            overwrite_choice = input(
                overwrite_info.format(pascalcase(quantity_name)))

            if overwrite_choice not in ['y', 'Y', 'yes', 'Yes']:
                return

        self._quantity_manager.new_quantity(quantity_name)

        base_unit = input(
            'Enter the name of the base unit of \'{0}\': '
            .format(quantity_name))

        self._quantity_manager.set_base_unit(base_unit)

        abbreviation = input(
            'Enter the abbreviation for \'{0}\': '
            .format(base_unit))

        self._quantity_manager.add_unit(base_unit, '1', abbreviation)

    def _add_unit(self) -> None:
        if not self._quantity_manager.quantity_loaded:
            print('No quantity loaded.')
            return

        unit_name = input('Enter the unit name: ')
        unit_abbreviation = input('Enter the unit abbreviation: ')
        unit_factor = input('Enter the unit factor: ')

        self._quantity_manager.add_unit(
            unit_name, unit_factor, unit_abbreviation)

    def _add_operator(self) -> None:
        if not self._quantity_manager.quantity_loaded:
            print('No quantity loaded.')
            return

        op_type = input('Enter the operation type (mul/div): ')
        other_type = input('Enter the quantity type of the second operand: ')
        result_type = input('Enter the quantity type of the result: ')

        self._quantity_manager.add_operator(op_type, other_type, result_type)

    def _remove_unit(self) -> None:
        if not self._quantity_manager.quantity_loaded:
            print('No quantity loaded.')
            return

        self._quantity_manager.list_units(with_index=True)

        try:
            unit_index = int(
                input('Enter the index of the unit to be removed: '))
        except ValueError:
            print('*** the input must be a number')
            return

        delete_choice = input(
            'Do you really want to remove the unit \'{0}\' '
            .format(self._quantity_manager.unit_name_by_index(unit_index))
            + 'from quantity \'{0}\'? (y/N): '
            .format(self._quantity_manager.current_quantity_name))

        if delete_choice not in ['y', 'Y', 'yes', 'Yes']:
            return

        self._quantity_manager.remove_unit(unit_index)

    def _remove_operator(self) -> None:
        print('Removing of operators is not implemented, yet.')

    def _remove_quantity(self) -> None:
        quantity_name = input('Enter the name of the quantity to remove: ')

        delete_info = (
            'Do you really want to remove the quantity \'{0}\'? '
            + 'This will delete the quantity definition file for \'{0}\' from '
            + 'the file system. Proceed? (y/N): ')
        delete_choice = input(delete_info.format(pascalcase(quantity_name)))

        if delete_choice not in ('y', 'Y', 'yes', 'Yes'):
            return

        self._quantity_manager.remove_quantity(quantity_name)
