# Author: Lukas Halbritter <halbritl@informatik.uni-freiburg.de>
# Copyright 2020
from jinja2 import Environment, FileSystemLoader, StrictUndefined
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
        self._template_env = Environment(
            loader=FileSystemLoader(searchpath=template_directory),
            trim_blocks=True,
            lstrip_blocks=True,
            undefined=StrictUndefined)

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

    def _load_source_json(self):
        LOGGER.info("Loading source file.")
        with open(self._source) as source:
            self._quantities = json.load(source)

    def _generate_package_init(self):
        init_path = os.path.join(self._target_dir, '__init__.py')

        self._write_file(init_path, '')

    def _generate_quantities_init(self):
        quantities_init_path = os.path.join(self._quantities_dir, '__init__.py')

        content = self._render_template(
            'quantities_init', quantities=self._quantities)

        self._write_file(quantities_init_path, content)

    def _generate_quantities(self):
        LOGGER.info("Generating quantity files.")
        for quantity in self._quantities:
            self._generate_quantity_module(quantity)

    def _generate_quantity_module(self, quantity):
        quantity_path = os.path.join(
            self._quantities_dir,
            self._decapitalize(quantity['name']) + '.py')

        content = self._render_template('quantity_module', quantity=quantity)

        self._write_file(quantity_path, content)

    def _generate_units_init(self):
        units_init_path = os.path.join(self._units_dir, '__init__.py')

        content = self._render_template(
            'units_init', quantities=self._quantities)

        self._write_file(units_init_path, content)

    def _generate_units(self):
        LOGGER.info("Generating unit files.")
        for quantity in self._quantities:
            self._generate_unit_module(quantity)

    def _generate_unit_module(self, quantity):
        unit_path = os.path.join(
            self._units_dir,
            self._decapitalize(quantity['name']) + 'Unit.py')

        content = self._render_template('unit_module', quantity=quantity)

        self._write_file(unit_path, content)

    def _render_template(self, template_name: str, **kwargs) -> str:
        LOGGER.debug('Rendering template %s with %s', template_name, kwargs)
        return (self._template_env
                .get_template(template_name + '.py.tmpl')
                .render(**kwargs))

    def _write_file(self, path: str, content: str) -> None:
        LOGGER.info("Generating %s.", path)
        with open(path, 'w') as f:
            f.write(content)

    @staticmethod
    def _decapitalize(string: str):
        return string[0].lower() + string[1:]
