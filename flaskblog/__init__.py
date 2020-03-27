'''
packaging flask app instead of a module,
initialize applications and bring different componenets
'''
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from flaskblog.config import Config

# extension objs
db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
mail = Mail()

login_manager.login_view = 'users.login'  # funcion name of route
# so in this way, if user tries to access account page, direct to login
# by leaving query param: next=/account
login_manager.login_message_category = 'info'


def create_app(config_class=Config):
    '''
    extension object doesn't initially get bound to application
    using this design pattern, no application-specific state is stored
    on the extension object
    so one extension object can be used for multipe apps
    '''
    app = Flask(__name__)
    app.config.from_object(Config)

    # extension objs
    db.init_app(app)  # can treate db structure as class (Model)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    from flaskblog.users.routes import users
    from flaskblog.posts.routes import posts
    from flaskblog.main.routes import main
    from flaskblog.errors.handlers import errors

    app.register_blueprint(users)
    app.register_blueprint(posts)
    app.register_blueprint(main)
    app.register_blueprint(errors)

    return app
