from flask import render_template
from app import app


@app.route('/')
@app.route('/index')
def hello_world():
    return render_template("partials/home.html")
