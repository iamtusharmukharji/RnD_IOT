from datetime import datetime
from IotApp import app
from . import models
from . import schemas
from sqlalchemy.exc import DBAPIError
from sqlalchemy.orm import Session
from flask_pydantic import validate
from flask import render_template, url_for, redirect, request, abort


@app.route('/')
def index():
    return redirect(url_for('documentation'))


@app.route("/docs")
def documentation():
    print("hello")
    return render_template("docs.html")
