from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

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

