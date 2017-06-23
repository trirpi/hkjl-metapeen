#!/usr/bin/env python
import argparse
import getpass
import os
import sys
import unittest

from crawler.crawler import update_all_scores, update_total_score
from peen import db
from peen.models import User, Hacker, Site
from tests.test_basic import BasicTestCase

parser = argparse.ArgumentParser(description='Manage HKJL Metapeen application.')
parser.add_argument('command', metavar='command', type=str, nargs='?', default='run',
                    help='action to perform (setup, test, crawl)')
arg = parser.parse_args()


def test():
    """Run the unit tests."""
    suite = unittest.TestLoader().loadTestsFromTestCase(BasicTestCase)
    unittest.TextTestRunner(verbosity=2).run(suite)


def setup():
    """Run deployment tasks."""
    # create db
    from peen import create_app
    app = create_app(os.getenv('FLASK_CONFIG') or 'default')
    with app.app_context():
        db.create_all()

    # create admin user
    admin_name = input('Admin name: ')

    # get admin password
    admin_pass = getpass.getpass('Admin password: ')

    if admin_name is None or admin_pass is None:
        print('Please provide a username and password.')
        sys.exit(0)

    admin = User(username=admin_name)
    admin.set_password(admin_pass)

    sites_info = [
        {
            'short_name': 'ht',
            'full_name': 'Hack This',
            'explanation': 'Hack This',
            'weight': 1
        },
        {
            'short_name': 'hts',
            'full_name': 'Hack This Site',
            'explanation': 'Hack This Site',
            'weight': 1
        },
        {
            'short_name': 'cs',
            'full_name': 'Certified Secure',
            'explanation': 'Certified Secure (username or id)',
            'weight': 1
        },        {
            'short_name': 'rm',
            'full_name': 'Root Me',
            'explanation': 'Root Me',
            'weight': 1
        },
        {
            'short_name': 'nf',
            'full_name': 'Netforce',
            'explanation': 'Netforce (userid)',
            'weight': 1
        },
        {
            'short_name': 'otw',
            'full_name': 'Over The Wire',
            'explanation': 'Over The Wire (Wechall username)',
            'weight': 1
        }
    ]
    # create Site objects
    sites = [
        Site(short_name=site['short_name'],
             full_name=site['full_name'],
             add_site_explanation=site['explanation'],
             weight=site['weight'])
        for site in sites_info
    ]
    # save everything in db
    with app.app_context():
        db.session.add(admin)
        db.session.commit()
        for site in sites:
            db.session.add(site)
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
    'setup': setup,
    'test': test
}

if __name__ == '__main__':
    commands[arg.command]()
