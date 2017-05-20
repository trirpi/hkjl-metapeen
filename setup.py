#!/usr/bin/env python

""" startup file for development """

from setuptools import setup

setup(
    name='metapeen',
    packages=['crawler', 'crawler'],
    include_package_data=False,
    install_requires=[
        'Flask>=0.10.1',
        'flask-sqlalchemy',
        'flask-login',
        'bs4',
        'requests'
    ]
)
