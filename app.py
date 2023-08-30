"""Blogly application."""

import os

from flask import Flask, request, redirect, render_template
from flask_debugtoolbar import DebugToolbarExtension

from models import db, connect_db, User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    "DATABASE_URL", 'postgresql:///blogly')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

app.debug = True
debug = DebugToolbarExtension(app)


connect_db(app)


# TODO: where does this go?
db.create_all()

@app.get("/")
def homepage():
    """Redirect to list of all users."""

    return redirect("/")

@app.get("/users")
def display_users():
    """Show all users."""

    return render_template("user-listing.html")


@app.get("/users/new")
def new_user_form():
    """Display form to add new users."""

    return render_template("new-user-form.html")