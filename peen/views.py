from flask import render_template, redirect, url_for, flash, request

from peen import app, lm
from peen.orm.models import User, Hacker


@lm.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/')
def index():
    users = Hacker.query.order_by(Hacker.total_score).all()
    return render_template('index.html', users=users)

if __name__ == '__main__':
    app.run()
