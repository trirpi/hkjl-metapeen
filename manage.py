#!/usr/bin/env python
import argparse
import getpass
import os
import sys
import unittest

from crawler.crawler import update_all_scores, update_total_score
from peen import create_app, db
from peen.models import User, Hacker
from tests.test_basic import BasicTestCase

parser = argparse.ArgumentParser(description='Manage HKJL Metapeen application.')
parser.add_argument('command', metavar='command', type=str, nargs='?', default='run',
                    help='action to perform (deploy, run, test, crawl)')
arg = parser.parse_args()


def test():
    """Run the unit tests."""
    suite = unittest.TestLoader().loadTestsFromTestCase(BasicTestCase)
    unittest.TextTestRunner(verbosity=2).run(suite)




def deploy():
    """Run deployment tasks."""
    # create db
    from peen import create_app
    app = create_app(os.getenv('FLASK_CONFIG') or 'default')
    with app.app_context():
        db.create_all()

    # create admin user
    if sys.version_info >= (3, 0):
        admin_name = input('Admin name: ')
    else:
        admin_name = raw_input('Admin name: ')

    # get admin password
    admin_pass = getpass.getpass('Admin password: ')

    if admin_name is None or admin_pass is None:
        print('Please provide a username and password.')
        sys.exit(0)

    admin = User(username=admin_name)
    admin.set_password(admin_pass)

    with app.app_context():
        db.session.add(admin)
        db.session.commit()


def crawl():
    from peen import create_app
    app = create_app(os.getenv('FLASK_CONFIG') or 'default')
    with app.app_context():
        hackers = Hacker.query.all()

        for hacker in hackers:
            update_all_scores(hacker)
            update_total_score(hacker)

commands = {
    'crawl': crawl,
    'deploy': deploy,
    'test': test
}

if __name__ == '__main__':
    commands[arg.command]()
