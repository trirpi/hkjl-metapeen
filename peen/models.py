from werkzeug.security import check_password_hash, generate_password_hash

from peen import db


class Site(db.Model):
    """Sites that can be used."""

    __tablename__ = 'sites'
    id = db.Column(db.Integer, primary_key=True)
    short_name = db.Column(db.String)
    full_name = db.Column(db.String)

    add_site_explanation = db.Column(db.String)
    weight = db.Column(db.Integer)

    def get(self, short_name):
        return self.query.filter_by(short_name=short_name).first()

    def __repr__(self):
        return "Site: id={}, shortname={}, weight={}".format(self.id, self.short_name, self.weight)


class Hacker(db.Model):
    """Metapeen user with all his scores."""

    __tablename__ = 'hackers'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String)
    total_score = db.Column(db.Integer)  # total score with weights

    def __init__(self):
        self.total_score = 0

    def get_site_account(self, short_site_name):
        return self.accounts.filter_by(short_site_name=short_site_name).first()

    def get_score(self, site):
        return self.get_site_account(site).score

    def get_relative_score(self, site):
        score = self.get_site_account(site).get_relative_score()
        return score

    def update_score(self, site, new_score):
        """Update score without weights from site."""
        self.get_site_account(site).update_score(new_score)

    def update_total_score(self):
        """Update total score of all sites with weights."""
        total_score = 0
        for account in self.accounts.all():
            total_score += self.get_relative_score(account.short_site_name)
        self.total_score = int(total_score)
        db.session.commit()

    def add_site_account(self, specific_username, site):
        account = Account(specific_username, site, self)
        self.accounts.append(account)
        db.session.commit()

    def get_optional_sites(self):
        sites = Site.query.all()
        registered_sites = []
        for account in self.accounts:
            registered_sites.append(account.site)
        return [x for x in sites if x not in registered_sites]

    @staticmethod
    def remove_site_account(site_id):
        account = Account.query.get(site_id)
        if account is not None:
            db.session.delete(account)
        db.session.commit()

    def __repr__(self):
        return "Hacker: id='{}', username='{}'".format(self.id, self.username)


class Account(db.Model):
    """Stores info of hacker accounts"""

    def __init__(self, specific_username, site, hacker):
        self.score = 0
        self.specific_username = specific_username

        self.site = site
        self.short_site_name = site.short_name

        self.user = hacker

    __tablename__ = 'accounts'
    id = db.Column(db.Integer, primary_key=True)
    specific_username = db.Column(db.String)
    score = db.Column(db.Integer)

    short_site_name = db.Column(db.String)
    site = db.relationship('Site', backref=db.backref('accounts', lazy='dynamic'))
    site_id = db.Column(db.Integer, db.ForeignKey('sites.id'))

    user = db.relationship('Hacker', backref=db.backref('accounts', lazy='dynamic'))
    user_id = db.Column(db.Integer, db.ForeignKey('hackers.id'))

    def update_score(self, new_score):
        self.score = new_score

    def get_relative_score(self):
        weight = self.site.weight
        return self.score * weight

    def __repr__(self):
        return "Account for {}: username='{}', score='{}'".format(self.short_site_name, self.specific_username, self.score)


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
