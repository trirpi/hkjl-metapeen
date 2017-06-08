from flask import jsonify

from peen import models
from . import api


@api.route('/hacker/<int:id>')
def get_hacker(id):
    hacker = models.Hacker.query.get(id)
    hacker_info = dict((c.name, getattr(hacker, c.name)) for c in hacker.__table__.columns)
    return jsonify(hacker_info)


@api.route('/hackers', methods=['GET'])
def get_hacker_list():
    hackers = models.Hacker.query.all()
    return jsonify([dict((c.name, getattr(hacker, c.name)) for c in hacker.__table__.columns) for hacker in hackers])
