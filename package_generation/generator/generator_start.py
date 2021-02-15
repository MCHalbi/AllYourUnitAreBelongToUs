# Author: Lukas Halbritter <halbritl@informatik.uni-freiburg.de>
# Copyright 2020
import argparse
import json
import logging.config
from generator import Generator

with open('logging.json') as json_file:
    logging_configuration = json.load(json_file)

logging.config.dictConfig(logging_configuration)


def parse_arguments():
    parser = argparse.ArgumentParser(
        description='Generates the ayuabtu package from a json file.')

    parser.add_argument(
        '-s', '--source',
        default='../quantity_definitions/',
        type=str,
        help='The path to the directory with quantity specifications from '
             'which the package should be generated.')

    parser.add_argument(
        '-d', '--templates',
        default='../templates/',
        type=str,
        help='The path to the template directory with templates for the module '
             'files.')

    parser.add_argument(
        '-t', '--target',
        default='../../ayuabtu/',
        type=str,
        help='The path to the directory in which the package should be '
             'generated. If the directory does not exist, it is created.')

    parser.add_argument(
        '-f', '--force',
        action='store_true',
        help='Overwrite existing files and directories.')

    return parser.parse_args()


def main():
    args = parse_arguments()

    generator = Generator(args.source, args.target, args.templates)
    generator.run(args.force)

if __name__ == '__main__':
    main()
