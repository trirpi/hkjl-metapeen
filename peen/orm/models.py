from peen import db
import site_weights

from sqlalchemy.ext.mutable import Mutable


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

    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String)
    scores = db.Column(MutableDict.as_mutable(db.PickleType))

    def get_rank(self):
        scores = [(x.username, x.get_score()) for x in Hacker.query.all()]  # this is a list of tuples so it can be sorted easily
        sorted_scores = dict(scores.sort(key=lambda x: x[1]))
        return sorted_scores[self.username]

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
                    scores = [self.scores[site][0], int(round(site_weights.callbacks[site]*self.scores[site][1]))]  # apply weights to list + round to nearest integer
                    return scores
                return self.scores[site]  # just return the list without weights
            else:
                callbacks = {
                    'name': 0,
                    'score': 1
                }
                if relative:
                    return int(round(self.scores[site][callbacks[info]]*site_weights.callbacks[site]))  # apply weights and round to nearest integer
                return self.scores[site][callbacks[info]]

        except KeyError:
            return None

    def get_score(self):
        return sum([int(x[1]) for x in list(self.scores.values())])

    def __repr__(self):
        return "<User(id='{}', username='{}')".format(self.id, self.username)


class User(db.Model):
    """ This is the admin user """

