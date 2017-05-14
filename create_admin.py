from peen.orm.models import User
from peen import db

admin_name = 'admin_oke'
admin_pass = 'okeisgoed'

admin = User(username=admin_name)
admin.set_password(admin_pass)

db.session.add(admin)
db.session.commit()
