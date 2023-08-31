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
        nullable=False
    )

    content = db.Column(
        db.String(40000),
        nullable=False
    )

    created_at = db.Column(
        db.DateTime,
        nullable=False,
        default=db.func.now
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey(User.id),
    )