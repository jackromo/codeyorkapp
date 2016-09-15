from flask import render_template, flash, redirect, session, url_for, request, g, jsonify
from flask_login import login_user, logout_user, current_user, login_required
from app import app, login_manager, db
from forms import LoginForm, SignupForm
from models import User, UserAssignments, Assignment
from testcode import get_test_str, check_test_results


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
        print user.username, user.email, user.password
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
        user.solve_assignment(assignment, result_path)
        db.session.commit()
    return jsonify({'solved': has_solved})


@app.errorhandler(404)
def not_found_editor(error):
    db.session.rollback()
    return render_template("partials/404.html"), 404


@app.errorhandler(500)
def not_found_editor(error):
    db.session.rollback()
    return render_template("partials/500.html"), 500
