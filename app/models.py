from app import db
from hashlib import md5
import os
import datetime


class User(db.Model):
    """
    Configuration for table of user accounts.

    Columns:
        id (int): Unique ID for a user.
        nickname (str): String name seen by others.
        email (str): Email account of user.
        password (str): Password of user.

    Relationships:
        asgn_solutions (UserAssignments, many-to-many): Solutions to assignments user has made.
    """

    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(128), index=True, unique=True)
    password = db.Column(db.String(64))
    asgn_solutions = db.relationship('UserAssignments', back_populates='user')

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

    def has_solved(self, assignment):
        return UserAssignments.query.filter(
            UserAssignments.asgn_id == assignment.id,
            UserAssignments.user_id == self.id
        ).first() is not None

    def solve_assignment(self, assignment, solution_dir):
        """
        Add solution from user for assignment, or amend old solution.
        Solution should be in solution_dir path already.
        Session must be committed after usage.
        """
        if self.has_solved(assignment):
            UserAssignments.query.filter(
                UserAssignments.user_id == self.id,
                UserAssignments.asgn_id == assignment.id
            ).first().result_dir = solution_dir
        else:
            asgn_sol = UserAssignments(user_id=self.id, asgn_id=assignment.id, result_dir=solution_dir)
            self.asgn_solutions.append(asgn_sol)
        return self

    def get_solved_assignments(self):
        return [asgn_sol.assignment for asgn_sol in self.asgn_solutions]

    def get_num_solved(self):
        return len(self.get_solved_assignments())

    def get_unsolved_visible_assignments(self):
        solved_asgns = self.get_solved_assignments()
        return [asgn for asgn in Assignment.query.filter(Assignment.visible == True) if asgn not in solved_asgns]

    def get_num_unsolved_visible(self):
        return len(self.get_unsolved_visible_assignments())

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
        date_due (Date): Date assignment is due. Due at the midnight at the start of that day, UTC time.
        tester_dir (str): Directory of tester script for assignment.

    Relationships:
        users_solved (UserAssignments, many-to-many): Users who have solved this assignment.
        asgn_tests (AssignmentTest, one-to-many): Tests for this assignment.
    """

    __tablename__ = 'assignments'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64), index=True, unique=True)
    desc = db.Column(db.String(300), index=True)
    visible = db.Column(db.Boolean)
    date_due = db.Column(db.Date)
    users_solved = db.relationship('UserAssignments', back_populates='assignment')
    asgn_tests = db.relationship('AssignmentTest', back_populates='assignment')

    def __repr__(self):
        return '<Assignment \"%s\">' % self.title

    def due_date_passed(self):
        datetime_due = datetime.datetime.fromordinal(self.date_due.toordinal())
        return (datetime.datetime.utcnow() - datetime_due).total_seconds() > 0


class UserAssignments(db.Model):
    """
    Programming solution of users to an assignment.
    Acts as many-to-many relationship between User and Assignment, including extra 'solution_dir' data.

    Columns:
        user_id (int): ID of user.
        asgn_id (int): ID of completed assignment.
        result_dir (str): Directory of program user has written.

    Relationships:
        user (User, many-to-many): User who solved an assignment.
        assignment (Assignment, many-to-many): Assignment user has solved.
    """

    __tablename__ = 'user_asgns'
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    asgn_id = db.Column(db.Integer, db.ForeignKey('assignments.id'), primary_key=True)
    result_dir = db.Column(db.String(120), index=True, unique=True)
    user = db.relationship('User', back_populates='asgn_solutions')
    assignment = db.relationship('Assignment', back_populates='users_solved')

    def __repr__(self):
        return '<User %s with assignment \"%s\">' % (self.user_id, self.asgn_id)


class AssignmentTest(db.Model):
    """
    A single test for an assignment.
    Consists of set of inputs, newline delimited, and the expected printed output.

    Columns:
        id (int): ID of test.
        asgn_id (int): ID of assignment being tested.
        test_inp (str): String of inputs to pass to program, line by line for each input()/raw_input() call.
        test_out (str): Expected output string.

    Relationships:
        assignment (Assignment, one-to-many): Assignment test is for.
    """

    __tablename__ = 'asgn_test'
    id = db.Column(db.Integer, primary_key=True)
    asgn_id = db.Column(db.Integer, db.ForeignKey('assignments.id'))
    test_inp = db.Column(db.String)
    test_out = db.Column(db.String)
    assignment = db.relationship('Assignment', back_populates='asgn_tests')

    def __repr__(self):
        return '<AssignmentTest %s for assignment %s>' % (self.id, self.assignment.title)

    def test_successful(self, result):
        return self.test_out == result
