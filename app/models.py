from app import db


class User(db.Model):
    """
    Configuration for table of user accounts.

    Contains:
        id (int): Unique ID for a user.
        nickname (str): String name seen by others.
        email (str): Email account of user.
        password (str): Encrypted password of user.
    """

    # TODO
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(128), index=True, unique=True)
    password = db.Column(db.String(64), index=True)

    def __repr__(self):
        return '<User %s>' % self.username
