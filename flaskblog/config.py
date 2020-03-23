import os


class Config:
    # app protects against modifying cookies..
    # >>> import secrets
    # >>> secrets.token_hex(16)
    #SECRET_KEY = os.environ.get('SECRET_KEY')
    SECRET_KEY = '58c137a362f6cd22dabecdf4ecf42ca8'
    #SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'

    # email extension
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    #MAIL_USERNAME = os.environ.get('EMAIL_USER')
    #MAIL_PASSWORD = os.environ.get('EMAIL_PASS')
    MAIL_USERNAME = 'cornercat2347@gmail.com'
    MAIL_PASSWORD = '2347stanford'
