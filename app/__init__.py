from flask import Flask
from flask_jwt_extended import JWTManager
from .db import db, migrate
from flask_cors import CORS
import os
from .models.user import User
from .models.post import Post
from .models.reply import Reply
from .models.like import Like
from .models.follow import Follow

# Import models, blueprints, and anything else needed to set up the app or database
from .routes.google_routes import bp as api_bp
from .routes.user_routes import bp as user_bp
from .routes.post_routes import bp as post_bp


def create_app(config=None):
    app = Flask(__name__)

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_DATABASE_URI')

    # Refresh & Access token configs
    app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY')  # load securely
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = 900   # 15 minutes
    app.config['JWT_REFRESH_TOKEN_EXPIRES'] = 86400 * 30  # 30 days

    jwt = JWTManager(app)   

    if config:
        app.config.update(config)

    # Initialize app with SQLAlchemy db and Migrate

    db.init_app(app)
    migrate.init_app(app, db)

    # Register Blueprints 

    app.register_blueprint(api_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(post_bp)

    CORS(app)
    return app