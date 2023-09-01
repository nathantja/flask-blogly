from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def connect_db(app):
    """Connect to database."""

    app.app_context().push()
    db.app = app
    db.init_app(app)


class User(db.Model):
    """User database model"""

    __tablename__ = "users"

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True)

    first_name = db.Column(
        db.String(30),
        nullable=False,)

    last_name = db.Column(
        db.String(30),
        nullable=False,)

    image_url = db.Column(
        db.Text,
        nullable=True,)


class Post(db.Model):
    """Blog post model"""

    __tablename__ = "posts"

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True)

    title = db.Column(
        db.String(300),
        nullable=False)

    content = db.Column(
        db.String(40000),
        nullable=False)

    created_at = db.Column(
        db.DateTime,
        nullable=False,
        default=db.func.now())

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"), # User.id
        nullable=False)

    user = db.relationship('User', backref= 'posts')
    tags = db.relationship('Tag', secondary='post_tags', backref= 'posts') #

class Tag(db.Model):
    """Tag model"""

    __tablename__ = "tags"

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True)

    name = db.Column(
        db.String(20),
        nullable=False
    )

class PostTag(db.Model):
    """Joined table of Post and Tag"""

    __tablename__ = "post_tags"

    post_id = db.Column(
        db.Integer,
        db.ForeignKey("posts.id"),
        nullable=False,
        primary_key=True
    )

    tag_id = db.Column(
        db.Integer,
        db.ForeignKey("tags.id"),
        nullable=False,
        primary_key=True
    )