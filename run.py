#!/usr/bin/env python
import argparse

from peen import create_app


parser = argparse.ArgumentParser(description='Run HKJL Metapeen application.')
parser.add_argument('--mode', dest='mode', default='default',
                    help='mode to run (production, test, development)')
parser.add_argument('--port', dest='port', default=5000,
                    help='port to run on')
parser.add_argument('--host', dest='host', default='127.0.0.1',
                    help='host to bind')
parser.add_argument('--secret_key', dest='secret_key', default='secret yay',
                    help='secret key (generate one with python -c "import os; print(os.urandom(24))"')
parser.add_argument('--debug', dest='debug', default='0',
                    help='start in debug mode')
args = parser.parse_args()


def run(mode):
    app = create_app(mode)
    app.run()

if __name__ == '__main__':
    run(args.mode)
