from flask import render_template
from app import app


@app.route('/')
@app.route('/index')
def home():
    return render_template("partials/home.html")


# TODO
@app.route('/login')
def login():
    return render_template("partials/login.html")


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
