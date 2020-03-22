'''
packaging flask app instead of a module,
initialize applications and bring different componenets
'''

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)
# app protects against modifying cookies..
# >>> import secrets
# >>> secrets.token_hex(16)
app.config['SECRET_KEY'] = '58c137a362f6cd22dabecdf4ecf42ca8'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)  # can treate db structure as class (Model)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'  # funcion name of route
# so in this way, if user tries to access account page, direct to login
# by leaving query param: next=/account
login_manager.login_message_category = 'info'

from flaskblog import routes
