from flask_restful import Resource, Api

from peen import app
from peen.orm import models

api = Api(app)


class Hacker(Resource):
    def get(self, hacker_id):
        hacker = models.Hacker.query.get(hacker_id)
        return dict((c.name, getattr(hacker, c.name)) for c in hacker.__table__.columns)


class HackerList(Resource):
    def get(self):
        hackers = models.Hacker.query.all()
        return [dict((c.name, getattr(hacker, c.name)) for c in hacker.__table__.columns) for hacker in hackers]


api.add_resource(Hacker, '/api/user/<string:hacker_id>')
api.add_resource(HackerList, '/api/users')

