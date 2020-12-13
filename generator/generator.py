# Author: Lukas Halbritter <halbritl@informatik.uni-freiburg.de>
# Copyright 2020
import json
import logging
import os
import shutil

LOGGER = logging.getLogger(__name__)


class Generator:
    def __init__(
            self,
            source_file: str,
            target_directory: str,
            template_directory: str) -> None:
        self._source = source_file
        self._target_dir = target_directory
        self._template_dir = template_directory

    def run(self, force_overwrite: bool) -> None:
        self._create_directory_structure(force_overwrite)
        self._generate_modules()

    def _create_directory_structure(self, force_overwrite: bool) -> None:
        if os.path.exists(self._target_dir):
            self._raise_error_if_target_is_no_directory()
            self._raise_error_if_force_is_false(force_overwrite)
            LOGGER.info('Removing existing target directory.')
            shutil.rmtree(self._target_dir)

        LOGGER.info('Creating %s.', self._target_dir)
        os.mkdir(self._target_dir)

        self._quantities_dir = os.path.join(self._target_dir, 'quantities')
        LOGGER.info('Creating %s.', self._quantities_dir)
        os.mkdir(self._quantities_dir)

        self._units_dir = os.path.join(self._target_dir, 'units')
        LOGGER.info('Creating %s.', self._units_dir)
        os.mkdir(self._units_dir)

    def _raise_error_if_target_is_no_directory(self):
        if not os.path.isdir(self._target_dir):
            raise NotADirectoryError(
                'The given target path exists but is no directory.')

    @staticmethod
    def _raise_error_if_force_is_false(force_overwrite):
        if not force_overwrite:
            raise FileExistsError(
                'The given target path already exists. '
                'Use --force to overwrite existing files and directories.')

    def _generate_modules(self, ):
        self._load_source_json()
        self._generate_package_init()
        self._generate_quantities_init()
        self._generate_quantities()
        self._generate_units_init()
        self._generate_units()

    def _generate_package_init(self):
        init_path = os.path.join(self._target_dir, '__init__.py')

        LOGGER.info('Generating %s.', init_path)
        open(init_path, 'a').close()

    def _load_source_json(self):
        LOGGER.info("Loading source file.")
        with open(self._source) as source:
            self._quantities = json.load(source)

    def _generate_quantities(self):
        LOGGER.info("Generating quantity files.")
        for quantity in self._quantities:
            self._generate_quantity_module(quantity)

    def _generate_quantity_module(self, quantity):
        module_string = self._quantity_module_string(quantity)
        quantity_path = os.path.join(
            self._quantities_dir,
            quantity['name'].lower() + '.py')

        LOGGER.info('Generating %s.', quantity_path)
        with open(quantity_path, 'w') as quantity_file:
            quantity_file.write(module_string)

    def _generate_quantities_init(self):
        quantities_init_path = os.path.join(self._quantities_dir, '__init__.py')
        LOGGER.info("Generating %s.", quantities_init_path)
        with open(quantities_init_path, 'w') as quantities_init_file:
            self._add_quantity_import_statements(quantities_init_file)

    def _add_quantity_import_statements(self, quantities_init_file):
        for quantity in self._quantities:
            self._add_quantity_import_statement(quantities_init_file, quantity)

    def _add_quantity_import_statement(self, quantities_init_file, quantity):
        import_statement = self._quantities_init_import_string(quantity['name'])

        LOGGER.debug('Adding import for %s.', quantity['name'])
        quantities_init_file.write(import_statement)

    def _generate_units(self):
        LOGGER.info("Generating unit files.")
        for quantity in self._quantities:
            self._generate_unit_module(quantity)

    def _generate_unit_module(self, quantity):
        unit_path = os.path.join(
            self._units_dir,
            quantity['name'].lower() + 'Unit.py')
        LOGGER.info('Generating %s.', unit_path)

        module_string = self._unit_module_string(quantity)

        with open(unit_path, 'w') as unit_file:
            unit_file.write(module_string)

    def _unit_module_string(self, quantity) -> str:
        module_template = self._read_template('module')

        return module_template.format(
            content=self._unit_module_content_string(quantity))[:-1]

    def _unit_module_content_string(self, quantity) -> str:
        unit_module_template = self._read_template('unit_module')

        return unit_module_template.format(
            quantity=quantity['name'],
            units=self._units_string(quantity))

    def _units_string(self, quantity) -> str:
        units_string = ''

        for index, unit in enumerate(quantity['units']):
            LOGGER.debug('Adding unit %s.', unit['name'])
            units_string += self._unit_string(unit, index)

        return units_string[:-1]

    def _unit_string(self, unit, index: int) -> str:
        unit_template = self._read_template('unit')

        return unit_template.format(
            unit_upper=unit['name'].upper(),
            index=str(index))

    def _generate_units_init(self):
        units_init_path = os.path.join(self._units_dir, '__init__.py')
        LOGGER.info("Generating %s.", units_init_path)
        with open(units_init_path, 'w') as units_init_file:
            self._add_units_import_statements(units_init_file)

    def _add_units_import_statements(self, units_init_file):
        for quantity in self._quantities:
            self._add_unit_import_statement(units_init_file, quantity)

    def _add_unit_import_statement(self, quantity_init_file, quantity):
        import_statement = self._units_init_import_string(quantity['name'])

        LOGGER.debug('Adding import for %s.', quantity['name'] + 'Unit')
        quantity_init_file.write(import_statement)

    def _units_init_import_string(self, quantity: str) -> str:
        units_import_template = self._read_template('units_init')

        return units_import_template.format(
            quantity=quantity, quantity_lower=quantity.lower())

    def _quantities_init_import_string(self, quantity: str) -> str:
        quantities_import_template = self._read_template('quantities_init')

        return quantities_import_template.format(
            quantity=quantity, quantity_lower=quantity.lower())

    def _quantity_module_string(self, quantity) -> str:
        module_template = self._read_template('module')

        return module_template.format(
            content=self._quantity_module_content_string(quantity))[:-1]

    def _quantity_module_content_string(self, quantity) -> str:
        quantity_module_template = self._read_template('quantity_module')

        return quantity_module_template.format(
            quantity=quantity['name'],
            base_unit_upper=quantity['baseunit'].upper(),
            factors=self._factors_string(quantity),
            abbreviations=self._abbreviations_string(quantity))

    def _factors_string(self, quantity) -> str:
        return ''.join(
            [self._factor_string(quantity, unit)
             for unit in quantity['units']])[:-1]

    def _factor_string(self, quantity, unit):
        factor_template = self._read_template('factor')

        return factor_template.format(
            quantity=quantity['name'],
            unit_upper=unit['name'].upper(),
            factor=unit['factor'])

    def _abbreviations_string(self, quantity) -> str:
        return ''.join(
            [self._abbreviation_string(quantity, unit)
             for unit in quantity['units']])[:-1]

    def _abbreviation_string(self, quantity, unit):
        abbreviation_template = self._read_template('abbreviation')

        return abbreviation_template.format(
            quantity=quantity['name'],
            unit_upper=unit['name'].upper(),
            abbreviation=unit['abbreviation'])

    def _read_template(self, file_name: str) -> str:
        file_name, extension = os.path.splitext(file_name)
        template_path = os.path.join(self._template_dir, file_name + '.tmpl')
        with open(template_path) as template_file:
            return template_file.read()
