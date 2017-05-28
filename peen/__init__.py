#!/usr/bin/env python

""" Handles all the setup for app."""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import configs

db = SQLAlchemy()

lm = LoginManager()
lm.login_view = 'admin.views.login'


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(configs[config_name])


    import peen.views
    import peen.admin.views
