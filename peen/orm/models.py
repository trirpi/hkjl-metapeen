from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy.ext.mutable import MutableDict

from peen import db
from site_weights import site_weights


class AccountInfo(object):
    """Stores information about site from a specific user."""
    def __init__(self, username, score=0):
        self.username = username
        self.score = score

    def update_score(self, new_score):
        self.score = new_score

    def get_relative_score(self, site):
        weight = site_weights[site]
        return self.score * weight

    def __repr__(self):
        return "Account Info: username='{}', score='{}'".format(self.username, self.score)


class Hacker(db.Model):
    """Metapeen user with all his scores."""

    __tablename__ = 'hackers'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String)
    accounts_info = db.Column(MutableDict.as_mutable(db.PickleType))  # mutable so it auto detects changes
    total_score = db.Column(db.Integer)  # total score with weights

    def __init__(self, username):
        self.username = username
        self.accounts_info = {}  # create dictionary
        db.session.commit()
        self.update_total_score()

    def get_score(self, site):
        return self.accounts_info[site].score

    def get_site_names(self):
        return self.accounts_info.keys()

    def get_relative_score(self, site):
        score = self.accounts_info[site].get_relative_score(site)
        return score

    def get_specific_username(self, site):
        return self.accounts_info[site].username

    def update_score(self, site, new_score):
        """Update score without weights from site."""
        self.accounts_info[site].update_score(new_score)

    def update_total_score(self):
        """Update total score of all sites with weights."""
        total_score = 0
        for score_site in self.accounts_info:
            total_score += self.get_relative_score(score_site)
        self.total_score = int(total_score)
        db.session.commit()

    def add_site(self, site, username):
        self.accounts_info[site] = AccountInfo(username)
        db.session.commit()

    def remove_site(self, site):
        del(self.accounts_info[site])
        db.session.commit()

    def __repr__(self):
        return "Hacker: id='{}', username='{}'".format(self.id, self.username)


class User(db.Model):
    """The admin user"""

    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String)
    password = db.Column(db.String)

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False  # application doesn't support anonymous users

    def get_id(self):
        return self.id

    def set_password(self, new_password):
        self.password = generate_password_hash(new_password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return "User: id='{}', username='{}'".format(self.id, self.username)
