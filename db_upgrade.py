"""
Helper script to upgrade the database to the next version, using migrate scripts.

Source: http://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-iv-database
"""

from migrate.versioning import api
from config import SQLALCHEMY_DATABASE_URI
from config import SQLALCHEMY_MIGRATE_REPO


if __name__ == '__main__':
    api.upgrade(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
    v = api.db_version(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
    print('Current database version: ' + str(v))
