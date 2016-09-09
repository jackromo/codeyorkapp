from flask import render_template, flash, redirect, session, url_for, request, g
from flask_login import login_user, logout_user, current_user, login_required
from app import app, login_manager, db
from forms import LoginForm, SignupForm
from models import User


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
    return render_template("partials/profile.html",
                           user=g.user)


@app.route('/resources')
def resources():
    return render_template("partials/resources.html")


# TODO
@app.route('/editor')
def editor():
    return render_template("partials/editor.html")
