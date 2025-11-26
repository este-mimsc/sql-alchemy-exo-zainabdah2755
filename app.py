"""Minimal Flask application setup for the SQLAlchemy assignment."""
from flask import Flask, jsonify, request
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from config import Config
from models import db, User, Post
# These extension instances are shared across the app and models
# so that SQLAlchemy can bind to the application context when the
# factory runs.
#db = SQLAlchemy()
migrate = Migrate()
def create_app(test_config=None):
    """Application factory used by Flask and the tests.

    The optional ``test_config`` dictionary can override settings such as
    the database URL to keep student tests isolated.
    """

    app = Flask(__name__)
    app.config.from_object(Config)
    if test_config:
        app.config.update(test_config)

    db.init_app(app)
    migrate.init_app(app, db)
# Import models here so SQLAlchemy is aware of them before migrations
# or ``create_all`` run. Students will flesh these out in ``models.py``.
    import models  # noqa: F401
    @app.route("/")
    def index():
        """Simple sanity check route."""
        return jsonify({"message": "Welcome to the Flask + SQLAlchemy assignment"})
    @app.route("/users", methods=["GET", "POST"])
    def users():
        """List or create users."""
        if request.method == "GET":
            users = User.query.all()
            data = [
                {"id": user.id, "username": user.username}
                for user in users
            ]
            return jsonify(data), 200
        if request.method == "POST":
            data = request.get_json()

            if not data or "username" not in data:
                return jsonify({"error": "Username is required"}), 400

            # Check if username already exists
            if User.query.filter_by(username=data["username"]).first():
                return jsonify({"error": "Username already exists"}), 400


            user = User(username=data["username"])
            db.session.add(user)
            db.session.commit()


            return jsonify({
                "id": user.id,
                "username": user.username
            }), 201


    @app.route("/posts", methods=["GET", "POST"])
    def posts():
        """List or create posts."""

        if request.method == "GET":
            posts = Post.query.all()
            data = []

            for post in posts:
                data.append({
                    "id": post.id,
                    "title": post.title,
                    "content": post.content,
                    "author": {
                        "id": post.author.id,
                        "username": post.author.username
                    }
                })

            return jsonify(data), 200

        if request.method == "POST":
            data = request.get_json()

            required_fields = {"title", "content", "user_id"}
            if not data or not required_fields.issubset(data):
                return jsonify({"error": "title, content and user_id are required"}), 400

            user = User.query.get(data["user_id"])
            if not user:
                return jsonify({"error": "User not found"}), 404

            post = Post(
                title=data["title"],
                content=data["content"],
                user_id=data["user_id"]
            )

            db.session.add(post)
            db.session.commit()

            return jsonify({
                "id": post.id,
                "title": post.title,
                "content": post.content,
                "user_id": post.user_id
            }), 201


    return app

# Expose a module-level application for convenience with certain tools
app = create_app()


if __name__ == "__main__":
    # Running ``python app.py`` starts the development server.
    app.run(debug=True)
