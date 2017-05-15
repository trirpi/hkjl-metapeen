import sys
from getpass import getpass

from peen.orm.models import User
from peen import db

# get admin username
admin_name = ''
if sys.version_info >= (3, 0):
    admin_name = input('Admin name: ')
else:
    admin_name = raw_input('Admin name: ')

# get admin password
admin_pass = getpass('Admin password: ')

if admin_name is None or admin_pass is None:
    print('Please provide a username and password.')
    sys.exit(0)

admin = User(username=admin_name)
admin.set_password(admin_pass)

db.session.add(admin)
db.session.commit()
