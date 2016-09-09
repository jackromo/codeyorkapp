from flask import render_template
from app import app
from forms import LoginForm, SignupForm


@app.route('/')
@app.route('/index')
def home():
    return render_template("partials/home.html")


# TODO
@app.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm()
    signup_form = SignupForm()
    return render_template("partials/login.html",
                           login_form=login_form,
                           signup_form=signup_form)


# TODO
@app.route('/signup', methods=['POST'])
def signup():
    pass


# TODO
@app.route('/profile')
def profile():
    return render_template("partials/profile.html")


@app.route('/resources')
def resources():
    return render_template("partials/resources.html")


# TODO
@app.route('/editor')
def editor():
    return render_template("partials/editor.html")
