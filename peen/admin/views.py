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


@admin.route('/', methods=['GET', 'POST'])
def main():
    """page where you can edit hackers"""
    return render_template('hackers.html',
                           hackers=Hacker.query.all(),
                           token_csrf=generate_csrf_token())


@admin.route('/edit_hacker/<int:hacker_id>', methods=['GET', 'POST'])
def edit_hacker(hacker_id):
    return render_template('edit_hacker.html',
                           hacker=Hacker.query.get(hacker_id),
                           token_csrf=generate_csrf_token())


@admin.route('/add_hacker', methods=['POST'])
def add_hacker():
    new_hacker = Hacker()
    new_hacker.username = request.form.get('username')
    db.session.add(new_hacker)
    db.session.commit()

    return redirect(url_for('.main'))


@admin.route('/add_site/<int:hacker_id>', methods=['POST'])
def add_site(hacker_id):
    hacker = Hacker.query.get(hacker_id)
    specific_username = request.form.get('specific_username') or hacker.username  # if nothing is provide take normal username
    hacker.add_site_account(request.form.get('site'), specific_username)

    return redirect(url_for('.edit_hacker', hacker_id=hacker_id))


@admin.route('/delete/<int:hacker_id>/', methods=['POST'])
def delete_hacker(hacker_id):
    hacker = Hacker.query.get(hacker_id)
    if hacker is not None:  # if it exists
        db.session.delete(hacker)
        db.session.commit()

    return redirect(url_for('.main'))


@admin.route('/delete_site/<int:hacker_id>', methods=['POST'])
def delete_site(hacker_id):
    hacker = Hacker.query.get(hacker_id)
    if hacker is not None:
        hacker.remove_site_account(request.form.get('site'))

    return redirect(url_for('.edit_hacker', hacker_id=hacker_id))
