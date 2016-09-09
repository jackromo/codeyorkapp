from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import basedir, ADMINS, MAIL_SERVER, MAIL_PORT, MAIL_USERNAME, MAIL_PASSWORD
import logging
from logging.handlers import SMTPHandler


app = Flask(__name__)
app.config.from_object('config')

db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# mail server init
if not app.debug:
    credentials = (MAIL_USERNAME, MAIL_PASSWORD) if MAIL_USERNAME or MAIL_PASSWORD else None
    mail_handler = SMTPHandler(
        (MAIL_SERVER, MAIL_PORT),
        'no-reply@' + MAIL_SERVER,
        ADMINS,
        'CodeYork app failure',
        credentials
    )
    mail_handler.setLevel(logging.ERROR)
    app.logger.addHandler(mail_handler)


from app import views, models
