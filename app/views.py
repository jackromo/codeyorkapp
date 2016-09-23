from flask import render_template, flash, redirect, session, url_for, request, g, jsonify
from flask_login import login_user, logout_user, current_user, login_required
from app import app, login_manager, db
from forms import LoginForm, SignupForm
from models import User, UserAssignments, Assignment, AssignmentTest
from testcode import get_test_str, check_test_results
from emails import send_email_users_new_asgn, send_email_admin_late_soln
from config import SECRET_KEY
import datetime


@app.before_request
def before_request():
    """
    Better access to current_user.
    """
    g.user = current_user


@app.route('/')
@app.route('/index')
def index():
    return render_template("partials/home.html")


@app.route('/login', methods=['GET', 'POST'])
def login():
    if g.user is not None and g.user.is_authenticated:
        return redirect(url_for('index'))
    login_form = LoginForm()
    signup_form = SignupForm()
    if login_form.validate_on_submit():
        user = User.query.filter_by(username=login_form.username.data).first()
        if user:
            # TODO: make password check more secure
            if user.password == login_form.password.data:
                login_user(user, remember=login_form.remember_me.data)
                return redirect(request.args.get('next') or url_for('index'))
        flash('Invalid username or password. Try again.')
        return redirect(url_for('login'))
    return render_template("partials/login.html",
                           login_form=login_form,
                           signup_form=signup_form)


@app.route('/signup', methods=['POST'])
def signup():
    signup_form = SignupForm()
    if signup_form.validate_on_submit():
        if User.query.filter_by(username=signup_form.username.data).first() \
                or User.query.filter_by(email=signup_form.email.data).first():
            flash('Username or email already taken. Try again.')
            return redirect(url_for('login'))
        user = User(
            username=signup_form.username.data,
            email=signup_form.email.data,
            password=signup_form.password.data
        )
        db.session.add(user)
        db.session.commit()
        login_user(user, remember=signup_form.remember_me.data)
        return redirect(request.args.get('next') or url_for('index'))
    return redirect(url_for('login'))


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/profile')
@login_required
def profile():
    solved_asgns = g.user.get_solved_assignments()
    unsolved_visible_asgns = g.user.get_unsolved_visible_assignments()
    return render_template("partials/profile.html",
                           user=g.user,
                           solved_asgns=solved_asgns,
                           unsolved_visible_asgns=unsolved_visible_asgns)


@app.route('/resources')
def resources():
    return render_template("partials/resources.html")


@app.route('/editor/<int:asgn_id>')
def editor(asgn_id):
    assignment = Assignment.query.filter(Assignment.id == asgn_id).first()
    user_soln = ''
    if g.user.has_solved(assignment):
        with open('./results/' + str(g.user.id) + '_' + str(asgn_id) + '.py', 'r') as f:
            user_soln = f.read()
    return render_template("partials/editor.html",
                           assignment=assignment,
                           user_soln=user_soln)


@app.route('/gettest/<int:asgn_id>', methods=['POST'])
def gettest(asgn_id):
    """
    Request for assignment tests when 'Submit' is hit in editor.
    """
    assignment = Assignment.query.filter(Assignment.id == asgn_id).first()
    test_prog_str = get_test_str(assignment)
    return jsonify({'test_template': test_prog_str})


@app.route('/testdone/<int:asgn_id>/<int:user_id>', methods=['POST'])
def testdone(asgn_id, user_id):
    """
    Request for test result verification once tests have been run; if successful, store user code.
    """
    user = User.query.filter(User.id == user_id).first()
    assignment = Assignment.query.filter(Assignment.id == asgn_id).first()
    req_json = request.get_json(silent=True)
    test_results = req_json['test_result']
    code_str = req_json['program']
    has_solved = check_test_results(assignment, test_results)
    if has_solved:
        result_path = './results/' + str(user_id) + '_' + str(asgn_id) + '.py'
        with open(result_path, 'w+') as f:
            f.write(code_str)
        if assignment.due_date_passed() and not user.has_solved(assignment):
            send_email_admin_late_soln(user, assignment)
        user.solve_assignment(assignment, result_path)
        db.session.commit()
    return jsonify({'solved': has_solved})


@app.route('/addassignment', methods=['POST'])
def addassignment():
    """
    Utility view for adding assignments.
    """
    req_json = request.get_json(silent=True)
    if not req_json:
        return "Assignment addition failed."
    if req_json['key'] != SECRET_KEY:
        return "Assignment addition failed; key incorrect."
    assignment = Assignment(
        title=req_json['title'],
        desc=req_json['desc'],
        visible=req_json['visible'],
        date_due=datetime.date.fromordinal(req_json['date_due'])
    )
    db.session.add(assignment)
    db.session.commit()
    if assignment.visible:
        send_email_users_new_asgn(assignment)
    return "Added assignment " + str(assignment) + " successfully."


@app.route('/delassignment', methods=['POST'])
def delassignment():
    """
    Utility view for deleting assignments.
    """
    req_json = request.get_json(silent=True)
    if not req_json:
        return "Assignment deletion failed."
    if req_json['key'] != SECRET_KEY:
        return "Assignment deletion failed; key incorrect."
    asgn = Assignment.query.filter(Assignment.id == req_json['asgn_id']).first()
    db.session.delete(asgn)
    return_str = "Assignment " + str(asgn) + " deleted successfully."
    db.session.commit()
    return return_str


@app.route('/getassignments', methods=['POST'])
def getassignments():
    """
    Utility view for retrieving list of all assignments.
    """
    req_json = request.get_json(silent=True)
    if not req_json:
        return "Assignment retrieval failed."
    if req_json['key'] != SECRET_KEY:
        return "Assignment retrieval failed; key incorrect."
    asgn_ls = []
    for asgn in Assignment.query.all():
        asgn_ls.append(
            "<id=%s title=\"%s\" desc=\"%s\" visible=%s datedue=%s>" % (
                str(asgn.id),
                asgn.title,
                asgn.desc,
                str(asgn.visible),
                str(asgn.date_due)
            )
        )
    return "\n".join(asgn_ls)


@app.route('/editassignment', methods=['POST'])
def editassignment():
    """
    Utility view for editing an assignment.
    """
    req_json = request.get_json(silent=True)
    if not req_json:
        return "Assignment editing failed."
    if req_json['key'] != SECRET_KEY:
        return "Assignment editing failed; key incorrect."
    asgn = Assignment.query.filter(Assignment.id == req_json['asgn_id']).first()
    if not asgn:
        return "Assignment editing fail; does not exist."
    asgn.title = req_json['title']
    asgn.desc = req_json['desc']
    asgn.visible = req_json['visible']
    asgn.date_due = datetime.date.fromordinal(req_json['date_due'])
    db.session.commit()
    if assignment.visible:
        send_email_users_new_asgn(assignment)
    return "Assignment edited successfully."


@app.route('/addtest', methods=['POST'])
def addtest():
    """
    Utility view for adding assignment tests.
    """
    req_json = request.get_json(silent=True)
    if not req_json:
        return "Test addition failed."
    if req_json['key'] != SECRET_KEY:
        return "Test addition failed; key incorrect."
    test = AssignmentTest(
        asgn_id=req_json['asgn_id'],
        test_inp=req_json['test_inp'],
        test_out=req_json['test_out'],
    )
    db.session.add(test)
    db.session.commit()
    return "Added assignment test " + str(test) + " successfully."


@app.route('/deltest', methods=['POST'])
def deltest():
    """
    Utility view for deleting assignment tests.
    """
    req_json = request.get_json(silent=True)
    if not req_json:
        return "Assignment deletion failed."
    if req_json['key'] != SECRET_KEY:
        return "Assignment deletion failed; key incorrect."
    test = AssignmentTest.query.filter(AssignmentTest.id == req_json['test_id']).first()
    return_str = "Assignment test" + str(test) + " deleted successfully."
    db.session.delete(test)
    db.session.commit()
    return return_str


@app.route('/getalltests', methods=['POST'])
def getalltests():
    """
    Utility view for retrieving list of all assignment tests.
    """
    req_json = request.get_json(silent=True)
    if not req_json:
        return "Test retrieval failed."
    if req_json['key'] != SECRET_KEY:
        return "Test retrieval failed; key incorrect."
    test_ls = []
    for test in AssignmentTest.query.all():
        test_ls.append(
            "<id=%s asgn_id=%s test_inp=\"%s\" test_out=\"%s\">" % (
                str(test.id),
                str(test.asgn_id),
                test.test_inp,
                test.test_out
            )
        )
    return "\n".join(test_ls)


@app.errorhandler(404)
def not_found_editor(error):
    db.session.rollback()
    return render_template("partials/404.html"), 404


@app.errorhandler(500)
def not_found_editor(error):
    db.session.rollback()
    return render_template("partials/500.html"), 500
