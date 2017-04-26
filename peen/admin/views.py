from os import urandom
from binascii import b2a_hex
from flask import request, render_template, redirect, flash, url_for, session, abort
from flask_login import login_user, login_required, logout_user

from peen.orm.models import User, Hacker
from peen import app, lm


@app.before_request
def protect_csrf():
    if request.method == 'POST':
        token = session.pop('token_csrf', None)
        if not token or token != request.form.get('token_csrf'):
            abort(403)


def generate_csrf_token():
    if 'token_csrf' not in session:
        session['token_csrf'] = b2a_hex(urandom(15)).decode('utf8')
    return session['token_csrf']


@app.route('/login', methods=['GET', 'POST'])
def login():
    """handles user login"""
    if request.method == 'POST':
        user = User.query.filter_by(username=request.form.get('username')).first()
        if user:
            if user.check_password(request.form.get('password')):
                login_user(user)
                flash('Logged in successfully.')
                return redirect(url_for('admin'))
        flash('Incorrect credentials.')
    return render_template('login.html', token_csrf=generate_csrf_token())

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/admin', methods=['GET', 'POST'])
@login_required
def admin():
    """main admin page"""
    return render_template('admin.html')

