from peen import app
from peen.orm import models



@api.route('/api/user/<int:id>')
def get_hacker(self, id):
    hacker = models.Hacker.query.get(id)
    hacker_info = dict((c.name, getattr(hacker, c.name)) for c in hacker.__table__.columns)
    return jsonify(hacker_info)


@api.route('/api/hackers', methods=['GET'])
def get_hacker_list(self):
    hackers = models.Hacker.query.all()
    return [dict((c.name, getattr(hacker, c.name)) for c in hacker.__table__.columns) for hacker in hackers]


api.add_resource(Hacker, '/api/user/<string:hacker_id>')
api.add_resource(HackerList, '/api/users')

