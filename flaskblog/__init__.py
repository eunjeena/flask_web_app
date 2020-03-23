'''
packaging flask app instead of a module,
initialize applications and bring different componenets
'''
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail

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

# email extension
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
#app.config['MAIL_USERNAME'] = os.environ.get('EMAIL_USER')
#app.config['MAIL_PASSWORD'] = os.environ.get('EMAIL_PASS')
app.config['MAIL_USERNAME'] = 'cornercat2347@gmail.com'
app.config['MAIL_PASSWORD'] = '2347stanford'
mail = Mail(app)

from flaskblog import routes
