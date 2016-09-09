import os


basedir = os.path.abspath(os.path.dirname(__file__))

# WTForm Config

WTF_CSRF_ENABLED = True
SECRET_KEY = 'i-totally-thought-of-a-good-key-m8-lmao-get-rekked-hax0rs'

# SQLite Config

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
SQLALCHEMY_TRACK_MODIFICATIONS = True  # set to True for debugging

# Mail Server Config

MAIL_SERVER = 'codeyorkapp.net'
MAIL_PORT = 25
MAIL_USERNAME = None
MAIL_PASSWORD = None

ADMINS = ['sharrackor@gmail.com']
