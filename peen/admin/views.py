from binascii import b2a_hex
from os import urandom

from flask import request, render_template, redirect, url_for, session, abort
from flask_login import current_user

from peen import db
from peen.models import User, Hacker
from . import admin


def generate_csrf_token():
    if 'token_csrf' not in session:
        session['token_csrf'] = b2a_hex(urandom(15)).decode('utf8')
    return session['token_csrf']


@admin.before_request
def protect_csrf():
    if request.method == 'POST':
        token = session.pop('token_csrf', None)
        if not token or token != request.form.get('token_csrf'):
            abort(403)


@admin.before_request
def check_user():
    if not current_user.is_authenticated:
        abort(401)


@admin.route('/')
def main():
    """main admin page"""
    return render_template('admin.html')


@admin.route('/edit_admins', methods=['GET', 'POST'])
def edit_admins():
    """page where you can edit admins"""
    return render_template('edit_admins.html', admins=User.query.all(), token_csrf=generate_csrf_token())


@admin.route('/edit_hackers', methods=['GET', 'POST'])
def edit_hackers():
    """page where you can edit hackers"""
    return render_template('edit_hackers.html',
                           hackers=Hacker.query.all(),
                           sites=['ht', 'hts', 'cs', 'otw', 'rm', 'nf'],
                           token_csrf=generate_csrf_token())


@admin.route('/add_hacker', methods=['POST'])
def add_hacker():
    new_hacker = Hacker()
    new_hacker.username = request.form.get('username')
    db.session.add(new_hacker)
    db.session.commit()

    return redirect(url_for('.edit_hackers'))


@admin.route('/add_site', methods=['POST'])
def add_site():
    hacker = Hacker.query.filter_by(username=request.form.get('username')).first()
    specific_username = request.form.get('specific_username') or hacker.username  # if nothing is provide take normal username
    hacker.add_site_account(request.form.get('site'), specific_username)

    return redirect(url_for('.edit_hackers'))


@admin.route('/delete_hacker', methods=['POST'])
def delete_hacker():
    hacker = Hacker.query.filter_by(username=request.form.get('username')).first()
    if hacker is not None:  # if it exists
        db.session.delete(hacker)
        db.session.commit()

    return redirect(url_for('.edit_hackers'))


@admin.route('/delete_site', methods=['POST'])
def delete_site():
    hacker = Hacker.query.filter_by(username=request.form.get('username')).first()
    if hacker is not None:
        hacker.remove_site_account(request.form.get('site'))

    return redirect(url_for('.edit_hackers'))
