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

    def get_info(self, site, info=None, relative=False):
        """
        Get score and/of username about specific site.
        :param site: short name for site (e.g. 'ht')
        :param info: 'name' or 'score' (empty for a list of both)
        :param relative: uses site_weights to determine how many points for the ranking it uses
        :return: score/username of site
        """
        try:
            if not info:
                if relative:
                    scores = [self.scores[site][0], int(round(crawler_config.callbacks[site] * self.scores[site][1]))]  # apply weights to list + round to nearest integer
                    return scores
                return self.scores[site]  # just return the list without weights
            else:
                callbacks = {
                    'name': 0,
                    'score': 1
                }
                if relative:
                    return int(round(self.scores[site][callbacks[info]] * crawler_config.callbacks[site]))  # apply weights and round to nearest integer
                return self.scores[site][callbacks[info]]  # same without weights

        except KeyError:
            return None

    def get_score(self):
        return sum([int(x[1]) for x in list(self.scores.values())])

    def __repr__(self):
        return "<Hacker(id='{}', username='{}')".format(self.id, self.username)


class User(db.Model):
    """ This is the admin user """

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
