from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy.ext.mutable import Mutable

from peen import db
import crawler_config


class MutableDict(Mutable, dict):
    """Class that makes PickleType detect changes."""
    @classmethod
    def coerce(cls, key, value):
        if not isinstance(value, MutableDict):
            if isinstance(value, dict):
                return MutableDict(value)
            return Mutable.coerce(key, value)
        else:
            return value

    def __delitem(self, key):
        dict.__delitem__(self, key)
        self.changed()

    def __setitem__(self, key, value):
        dict.__setitem__(self, key, value)
        self.changed()

    def __getstate__(self):
        return dict(self)

    def __setstate__(self, state):
        self.update(self)


class Hacker(db.Model):
    """Metapeen user with all his scores."""

    __tablename__ = 'hackers'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String)
    scores = db.Column(MutableDict.as_mutable(db.PickleType))
    total_score = db.Column(db.Integer)  # total score with weights

    def get_score(self, site, relative=False):
        """
        Get score about specific site.
        :param site: short name for site (e.g. 'ht')
        :param relative: uses site_weights to determine how many points for the ranking it uses
        :return: score of site
        """
        place_of_score = 1
        if relative:
            score = self.scores[site][place_of_score] * crawler_config.site_weights[site]  # apply weights to score
            return score
        else:
            return self.scores[site][place_of_score]

    def update_score(self, site, score):
        """Update score without weights from site."""
        self.scores[site] = [self.scores[site][0], score]  # set new values

    def update_total_score(self):
        """Update total score of all sites with weights."""
        total_score = 0
        for score_site in self.scores:
            total_score += self.get_score(score_site, relative=True)
        self.total_score = total_score
        db.session.commit()

    def add_site(self, site, username):
        self.scores[site] = [username, 0]

    def __repr__(self):
        return "<Hacker(id='{}', username='{}')".format(self.id, self.username)


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
        return "<User(id='{}', username='{}')".format(self.id, self.username)
