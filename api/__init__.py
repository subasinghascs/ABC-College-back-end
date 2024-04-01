from logging.handlers import RotatingFileHandler
import logging
from flask import Flask
from Database.db import db
from config import SECRET_KEY, SQLALCHEMY_DATABASE_URI
from flask_jwt_extended import JWTManager
from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = SECRET_KEY
    app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = 'your_secret_key'  # Change this in production
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = False
    db.init_app(app)
    jwt = JWTManager(app)
    CORS(app)  # Enable CORS for all routes

    # Configure logging
    configure_logging(app)

    with app.app_context():
        db.create_all()

    # Import blueprints
    from api.route.student_routes import student_bp
    from api.route.admin_routes import admin_bp

    # Register blueprints with unique names
    app.register_blueprint(student_bp, url_prefix='/api/student')
    app.register_blueprint(admin_bp, url_prefix='/api/admin')

    return app

def configure_logging(app):
    # Configure the root logger
    app.logger.setLevel(logging.INFO)

    # Create a rotating file handler for logging to a file
    file_handler = RotatingFileHandler('app.log', maxBytes=1024 * 1024 * 10, backupCount=5)
    file_handler.setLevel(logging.INFO)

    # Create a formatter and set it for the file handler
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)

    # Add the file handler to the root logger
    app.logger.addHandler(file_handler)

    # Disable Flask's default logger to prevent duplicate log messages
    app.logger.propagate = False
