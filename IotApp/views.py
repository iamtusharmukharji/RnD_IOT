from IotApp import app
from flask import render_template, url_for, redirect



@app.route('/')
def index():
    return redirect(url_for('documentation'))

@app.route("/docs")
def documentation():
    print("hello")
    return render_template("docs.html")
