from os import urandom
from binascii import b2a_hex
from flask import request, render_template, redirect, flash, url_for, session, abort
from flask_login import login_user, login_required, logout_user

from peen.orm.models import User, Hacker
from peen import app, db


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


@app.route('/admin')
@login_required
def admin():
    """main admin page"""
    return render_template('admin.html')


@app.route('/edit_admins', methods=['GET', 'POST'])
@login_required
def edit_admins():
    """page where you can edit admins"""
    return render_template('edit_admins.html', admins=User.query.all(), token_csrf=generate_csrf_token())


@app.route('/edit_hackers', methods=['GET', 'POST'])
@login_required
def edit_hackers():
    """page where you can edit hackers"""
    return render_template('edit_hackers.html', hackers=Hacker.query.all(), token_csrf=generate_csrf_token())


@app.route('/add_hacker', methods=['POST'])
@login_required
def add_hacker():
    new_hacker = Hacker(username=request.form.get('username'))
    db.session.add(new_hacker)
    db.session.commit()

    return redirect(url_for('edit_hackers'))


@app.route('/add_site', methods=['POST'])
@login_required
def add_site():
    hacker = Hacker.query.filter_by(username=request.form.get('username')).first()
    specific_username = request.form.get('specific_username') or hacker.username  # if nothing is provide take normal username
    hacker.add_site(request.form.get('site'), specific_username)

    return redirect(url_for('edit_hackers'))


@app.route('/delete_hacker', methods=['POST'])
@login_required
def delete_hacker():
    hacker = Hacker.query.filter_by(username=request.form.get('username')).first()
    if hacker is not None:  # if it exists
        db.session.delete(hacker)
        db.session.commit()

    return redirect(url_for('edit_hackers'))
