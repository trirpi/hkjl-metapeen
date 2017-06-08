from flask import flash, request, url_for, redirect, render_template
from flask_login import login_user, logout_user

from peen.models import User
from . import auth


@auth.route('/login', methods=['GET', 'POST'])
def login():
    """handles user login"""
    if request.method == 'POST':
        user = User.query.filter_by(username=request.form.get('username')).first()
        if user:
            if user.check_password(request.form.get('password')):
                login_user(user)
                flash('Logged in successfully.')
                return redirect(url_for('admin.main'))
        flash('Incorrect credentials.')
    return render_template('login.html')


@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))
