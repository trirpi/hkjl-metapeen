#!/usr/bin/env python
import argparse

from peen import create_app

parser = argparse.ArgumentParser(description='Run HKJL Metapeen application.')
parser.add_argument('mode', metavar='mode', type=str, nargs='?', default='default',
                    help='mode to run (production, test, development)')
args = parser.parse_args()


def run(mode):
    app = create_app(mode)
    app.run()

if __name__ == '__main__':
    run(args.mode)
