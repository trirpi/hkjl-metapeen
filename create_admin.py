import sys

from peen.orm.models import User
from peen import db

admin_name = ''
admin_pass = ''

if sys.version.info >= (3, 0):
    admin_name = input('Admin name: ')
    admin_pass = input('Admin password: ')
else:
    admin_name = raw_input('Admin name: ')
    admin_pass = raw_input('Admin password: ')

if admin_name is None or admin_pass is None:
    print('Please provide a username and password.')
    sys.exit(0)

admin = User(username=admin_name)
admin.set_password(admin_pass)

db.session.add(admin)
db.session.commit()
