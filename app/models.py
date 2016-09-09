from app import db
from hashlib import md5


class User(db.Model):
    """
    Configuration for table of user accounts.

    Columns:
        id (int): Unique ID for a user.
        nickname (str): String name seen by others.
        email (str): Email account of user.
        password (str): Password of user.
    """

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(128), index=True, unique=True)
    password = db.Column(db.String(64))

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return True

    def get_id(self):
        return unicode(self.id)

    def avatar(self, size):
        return 'http://gravatar.com/avatar/%s?d=mm&s=%d' % (md5(self.email.encode('utf-8')).hexdigest(), size)

    def __repr__(self):
        return '<User %s>' % self.username


class Assignment(db.Model):
    """
    Programming assignment, with task and tests.

    Columns:
        id (int): Unique ID of assignment.
        title (str): Title of assignment.
        desc (str): Description of assignment.
        visible (bool): Whether assignment is visible to users or not.
        tester_dir (str): Directory of tester script for assignment.
    """

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64), index=True, unique=True)
    desc = db.Column(db.String(300), index=True)
    visible = db.Column(db.Boolean)
    tester_dir = db.Column(db.String(120), index=True)

    def __repr__(self):
        return '<Assignment \"%s\">' % self.title


class UserAssignments(db.Model):
    """
    Programming solutions of users to each assignment.

    Columns:
        id (int): Unique ID of user program for assignment.
        user_id (int): ID of user.
        asgn_id (int): ID of completed assignment.
        result_dir (str):
    """

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, index=True)
    asgn_id = db.Column(db.Integer)
    result_dir = db.Column(db.String(120), index=True, unique=True)

    def __repr__(self):
        return '<User %s with assignment \"%s\">' % (self.user_id, self.asgn_id)
