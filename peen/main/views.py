from flask import render_template
from sqlalchemy import desc

from . import main
from peen import lm
from peen.models import User, Hacker


@lm.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@main.route('/')
def index():
    hackers = Hacker.query.order_by(desc(Hacker.total_score)).all()  # get hackers sorted on score
    return render_template('index.html', users=hackers)
