"""
Helper script to create a database called 'app.db'.

Source: http://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-iv-database
"""

from migrate.versioning import api
from config import SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO
from app import db
import os.path


if __name__ == '__main__':
    db.create_all()
    if not os.path.exists(SQLALCHEMY_MIGRATE_REPO):
        api.create(SQLALCHEMY_MIGRATE_REPO, 'database repository')
        api.version_control(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
    else:
        api.version_control(
            SQLALCHEMY_DATABASE_URI,
            SQLALCHEMY_MIGRATE_REPO,
            api.version(SQLALCHEMY_MIGRATE_REPO)
        )
