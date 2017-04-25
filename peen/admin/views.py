from flask import request, render_template, redirect, flash, url_for
from flask_login import login_user, login_required

from peen.orm.models import User, Hacker
from peen import app, lm


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


@app.route('/admin', methods=['GET', 'POST'])
@login_required
def admin():
    """main admin page"""
    return render_template('admin.html')
