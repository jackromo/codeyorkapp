from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import basedir, ADMINS, MAIL_SERVER, MAIL_PORT, MAIL_USERNAME, MAIL_PASSWORD
import logging
from logging.handlers import SMTPHandler, RotatingFileHandler


app = Flask(__name__)
app.config.from_object('config')

db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

if not app.debug:
    # mail server init
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
    # file logging init
    # 1 megabyte log files, keep last 10 log files as backup
    file_handler = RotatingFileHandler('log/codeyorkapp.log', 'a', 1 * 1024 * 1024, 10)
    file_handler.setFormatter(
        logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('CodeYork app startup')


from app import views, models
