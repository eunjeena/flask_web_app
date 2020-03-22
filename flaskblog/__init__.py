'''
packaging flask app instead of a module,
initialize applications and bring different componenets
'''

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
# app protects against modifying cookies..
# >>> import secrets
# >>> secrets.token_hex(16)
app.config['SECRET_KEY'] = '58c137a362f6cd22dabecdf4ecf42ca8'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)  # can treate db structure as class (Model)

from flaskblog import routes
