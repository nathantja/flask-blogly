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

app.config['SECRET_KEY'] = "super-secret"

app.debug = True
debug = DebugToolbarExtension(app)

app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False


connect_db(app)


@app.get("/")
def homepage():
    """Redirect to list of all users."""

    return redirect("/users")

@app.get("/users")
def display_users():
    """Show all users."""
    users = User.query.all()

    return render_template("user-listing.html", users = users)


@app.get("/users/new")
def new_user_form():
    """Display form to add new users."""

    return render_template("new-user-form.html")

@app.post("/users/new")
def process_user_form():
    """ Add user to database and show users page."""
    first_name = request.form.get("first-name")
    last_name = request.form.get("last-name")
    image_url = request.form.get("image-url")

    user = User(first_name = first_name,
                last_name = last_name,
                image_url = image_url)

    db.session.add(user)
    db.session.commit()

    return redirect("/users")

@app.get("/users/<int:id>")
def show_user(id):
    """Displays user information"""
    user = User.query.get(id)
    return render_template("user-detail-page.html", user = user)


@app.get("/users/<int:id>/edit")
def edit_user(id):
    """Display edit form"""

    return render_template("user-edit-page.html", id=id)


@app.post("/users/<int:id>/edit")
def process_edit_form(id):
    """Edit user info and save to database."""
    user = User.query.get(id)

    first_name = request.form.get("first-name")
    last_name = request.form.get("last-name")
    image_url = request.form.get("image-url")

    user.first_name = first_name
    user.last_name = last_name
    user.image_url = image_url

    db.session.commit()

    return redirect("/users")


@app.post("/users/<int:id>/delete")
def delete_user(id):
    """Delete user from database."""

    user = User.query.get(id)

    db.session.delete(user)
    db.session.commit()

    return redirect("/users")