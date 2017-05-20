#!/usr/bin/env python

""" Handles all the setup for app."""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_restful import Api


app = Flask(__name__)
app.config.from_object('config')

db = SQLAlchemy(app)
db.create_all()

lm = LoginManager()
lm.init_app(app)
lm.login_view = 'login'

api = Api(app)

import peen.views
import peen.admin.views
import peen.api.views
