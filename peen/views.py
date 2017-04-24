from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user

from peen import app, lm
from peen.orm.models import User, Hacker


@lm.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/login', methods=['GET', 'POST'])
def login():
    """handles user login on form"""
    if request.method == 'GET':
        return render_template('login.html')
    if request.method == 'POST':
        user = User.query.filter_by(username=request).first()
        login_user(user, remember=True)

        flash('Logged in successfully.')
        return redirect(url_for('index'))
    return render_template('login.html')


@app.route('/')
def index():
    users = Hacker.query.all()
    return render_template('index.html', users=users)

if __name__ == '__main__':
    app.run()
