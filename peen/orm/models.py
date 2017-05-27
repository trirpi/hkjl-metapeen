from werkzeug.security import check_password_hash, generate_password_hash

from peen import db
from site_weights import site_weights


class Hacker(db.Model):
    """Metapeen user with all his scores."""

    __tablename__ = 'hackers'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String)
    total_score = db.Column(db.Integer)  # total score with weights

    def __init__(self):
        self.total_score = 0

    def get_site_account(self, site):
        return self.accounts.filter_by(site=site).first()

    def get_score(self, site):
        return self.get_site_account(site).score

    def get_relative_score(self, site):
        score = self.accounts_info[site].get_relative_score(site)
        return score

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

    def add_site_account(self, site, specific_username):
        account = Account(specific_username=specific_username, site=site, score=0, user_id=self.id)
        self.accounts.append(account)
        db.session.commit()

    def remove_site_account(self, site):
        db.session.delete(self.get_site_account(site))
        db.session.commit()

    def __repr__(self):
        return "Hacker: id='{}', username='{}'".format(self.id, self.username)


class Account(db.Model):
    """Stores info of hacker accounts"""

    __tablename__ = 'accounts'
    id = db.Column(db.Integer, primary_key=True)
    site = db.Column(db.String)
    specific_username = db.Column(db.String)
    score = db.Column(db.Integer)

    user = db.relationship('Hacker', backref=db.backref('accounts', lazy='dynamic'))
    user_id = db.Column(db.Integer, db.ForeignKey('hackers.id'))

    def update_score(self, new_score):
        self.score = new_score

    def get_relative_score(self):
        weight = site_weights[self.site]
        return self.score * weight

    def __repr__(self):
        return "Account Info for {}: username='{}', score='{}'".format(self.site, self.specific_username, self.score)


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
