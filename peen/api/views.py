from flask_restful import Resource

from peen import api
from peen.orm import models


class Hacker(Resource):
    def get(self, hacker_id):
        hacker = models.Hacker.query.get(hacker_id)
        return dict((c.name, getattr(hacker, c.username)) for c in hacker.__table__.columns)


api.add_resource(Hacker, '/api/hacker/<string:hacker_id>')