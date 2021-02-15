# Author: Lukas Halbritter <halbritl@informatik.uni-freiburg.de>
# Copyright 2021
import argparse
from qm_shell import QMShell

def parse_arguments():
    parser = argparse.ArgumentParser(
        description='The Quantity Manager is used to manage all your quantity '
                    'definitions so you do not have to deal with the quantity '
                    'definition json files directly.')

    parser.add_argument(
        '-d', '--dir',
        default='../quantity_definitions/',
        type=str,
        help='The path to the directory containing the quantity definition '
             'files.')

    return parser.parse_args()

def main():
    args = parse_arguments()

    QMShell(args.dir).cmdloop()

if __name__ == '__main__':
    main()
