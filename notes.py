# sqlalchemy
'''
# create db
db.create_all() : creates {db} from sqlite:///{db}

# add user in db
user1 = User({username}, {email}, {pw})
db.session.add(user1); db.session.commit()

# see user in User db
User.query.all(); User.query.first()
User.query.filter_by(usename={}).all(){.first()}

# add post in db
post1 = Post({title}, {content}, use_id=user1.id)
p = Post.query.first()

# see whos post it is
p.author -> print out User's repr

# drop db
db.drop_all()
'''

# encrypt password
'''
from flask_bcrypt import Bcrypt
b = Bcrypt()

# create hashed pw
b.generate_password_hash("test")
b'$2b$12$LmLkxAzuIjKJ123bsKoC9uMHCfyRXhiVPvFQUySeFQNyWYmkkF.ou'
b.generate_password_hash("test").decode("utf-8")

# check if pw is correct
b.check_password_hash(hashed_pw, 'pass:user_typed')
return T/F
'''
