from app import db
from models import User, Admin

# db.create_all()'
# newobj = Admin(username="陈禹轲", email="1648109733@qq.com", password="022403Cyk")
# db.session.add(newobj)
# db.session.commit()
users = User.query.all()
print(users)
admins = Admin.query.all()
print(admins)