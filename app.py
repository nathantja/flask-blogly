"""Blogly application."""

import os

from flask import Flask, request, redirect, render_template
from flask_debugtoolbar import DebugToolbarExtension

from models import db, connect_db, User, Post

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


DEFAULT_IMG_URL = "https://upload.wikimedia.org/wikipedia/commons/b/b5/Windows_10_Default_Profile_Picture.svg"


@app.get("/")
def homepage():
    """Redirect to list of all users."""

    return redirect("/users")


@app.get("/users")
def display_users():
    """Show all users."""
    users = User.query.all()

    return render_template("user-listing.html", users=users)


@app.get("/users/new")
def new_user_form():
    """Display form to add new users."""

    return render_template("user-new-form.html")


@app.post("/users/new")
def process_user_form():
    """ Add user to database and show users page."""
    first_name = request.form.get("first-name")
    last_name = request.form.get("last-name")
    image_url = request.form.get("image-url", DEFAULT_IMG_URL)

    if not image_url:
        image_url = DEFAULT_IMG_URL
    # print('image_url', image_url)
    # breakpoint()

    user = User(first_name=first_name,
                last_name=last_name,
                image_url=image_url)

    db.session.add(user)
    db.session.commit()

    return redirect("/users")


@app.get("/users/<int:id>")
def show_user(id):
    """Displays user information"""
    user = User.query.get_or_404(id)
    return render_template("user-detail-page.html", user=user)


@app.get("/users/<int:id>/edit")
def edit_user(id):
    """Display edit form with values filled in."""
    user = User.query.get_or_404(id)
    return render_template("user-edit-page.html", user=user)


@app.post("/users/<int:id>/edit")
def process_edit_form(id):
    """Edit user info and save to database."""
    user = User.query.get_or_404(id)

    first_name = request.form.get("first-name")
    last_name = request.form.get("last-name")
    image_url = request.form.get("image-url")

    if not image_url:
        image_url = DEFAULT_IMG_URL

    user.first_name = first_name
    user.last_name = last_name
    user.image_url = image_url

    db.session.commit()

    return redirect("/users")


@app.post("/users/<int:id>/delete")
def delete_user(id):
    """Delete user from database."""

    user = User.query.get_or_404(id)

    db.session.delete(user)
    db.session.commit()

    return redirect("/users")


@app.get("/users/<int:id>/posts/new")
def new_post_form(id):
    """Render form to add post."""

    user = User.query.get_or_404(id)

    return render_template("post-new-form.html", user=user)


@app.post("/users/<int:id>/posts/new")
def process_post_form(id):
    """Save post to database."""

    post_title = request.form.get("content")
    post_content = request.form.get("title")

    post = Post(title=post_title, content=post_content, user_id=id)
    db.session.add(post)

    return redirect("/users/<int:id>")
