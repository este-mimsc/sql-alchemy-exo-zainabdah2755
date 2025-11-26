"""Database models for the blog assignment.

The attributes are left intentionally light so students can practice
adding the proper columns, relationships, and helper methods.
"""
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    """Represents a user who can author posts."""

    __tablename__ = "users"

    # TODO: Add id primary key, username (unique + required), and
    # a relationship to ``Post`` named ``posts``.
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String)  # Students should customize constraints
    posts = db.relationship("Post", backref="author", lazy=True)
    def __repr__(self):  # pragma: no cover - convenience repr
        return f"<User {getattr(self, 'username', None)}>"


class Post(db.Model):
    """Represents a blog post written by a user."""

    __tablename__ = "posts"

    # TODO: Add id primary key, title, content, foreign key to users.id,
    # and a relationship back to the ``User`` model.
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)


    def __repr__(self):  # pragma: no cover - convenience repr
        return f"<Post {getattr(self, 'title', None)}>"
