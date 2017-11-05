#!/usr/bin/env python

import argparse
import os
from peen import create_app

parser = argparse.ArgumentParser(description='Run HKJL Metapeen application.')
parser.add_argument('--port', dest='port', default='5000',
                    help='port to run on')
parser.add_argument('--host', dest='host', default='127.0.0.1',
                    help='host to bind')
parser.add_argument('--secret_key', dest='secret_key', default=os.urandom(24),
                    help='secret key (defaults to an automatically generated one with "import os; os.urandom(24))"')
args = parser.parse_args()

app_mode = os.getenv('FLASK_CONFIG') or 'default'


def run(mode):
    app = create_app(mode)
    app.config['SECRET_KEY'] = args.secret_key

    if mode == 'production':
        from gevent import monkey
        monkey.patch_all()

        from gevent.pywsgi import WSGIServer
        http_server = WSGIServer((args.host, int(args.port)), app)
        print(' * Running on http://%s:%s/ (Press CTRL+C to quit)' % (args.host, args.port))
        http_server.serve_forever()

    else:  # testing or development
        app.run(host=args.host, port=args.port)

if __name__ == '__main__':
    run(app_mode)
