#!/usr/bin/env python

""" startup file for development """

from setuptools import setup

setup(
    name='metapeen',
    packages=['admin', 'crawler'],
    include_package_data=False,
    install_requires=[
        'flask',
        'flask-sqlalchemy',
        'bs4',
        'requests'
    ]
)
