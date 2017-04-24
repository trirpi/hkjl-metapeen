# -*- coding: utf8 -*-
import os

basedir = os.path.abspath(os.path.dirname(__file__))

BIND_HOST = '127.0.0.1'
BIND_PORT = 5000

# db settings
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_TRACK_MODIFICATIONS = False
