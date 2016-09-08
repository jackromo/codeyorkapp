"""
Helper script to downgrade the database to the previous version, using migrate scripts.

Source: http://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-iv-database
"""

from migrate.versioning import api
from config import SQLALCHEMY_DATABASE_URI
from config import SQLALCHEMY_MIGRATE_REPO


if __name__ == '__main__':
    v = api.db_version(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
    api.downgrade(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO, v - 1)
    v = api.db_version(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
    print('Current database version: ' + str(v))