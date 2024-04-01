# app/routes.py

from flask import request, jsonify, Blueprint
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity
from werkzeug.security import check_password_hash, generate_password_hash
from Database.db import db
from api.model.admin_model import Admin

admin_bp = Blueprint('Admin', __name__)

@admin_bp.route('/signup', methods=['POST'])
def signup():
    if request.method == 'POST':
        first_name = request.json.get('first_name')
        last_name = request.json.get('last_name')
        username = request.json.get('username')
        password = request.json.get('password')
        existing_user = Admin.query.filter_by(username=username).first()
        if existing_user:
            return jsonify({"message": "User already exists"}), 409
        else:
            hashed_password = generate_password_hash(password)
            new_user = Admin(first_name=first_name, last_name=last_name, username=username, password=hashed_password)
            db.session.add(new_user)
            db.session.commit()
            return jsonify({"message": "User created successfully"}), 201

@admin_bp.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        username = request.json.get('username')
        password = request.json.get('password')
        user = Admin.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            access_token = create_access_token(identity=username)
            return jsonify({"access_token": access_token}), 200
        else:
            return jsonify({"message": "Invalid username or password"}), 401

@admin_bp.route('/protected-route')
@jwt_required()
def protected_route():
    current_user = get_jwt_identity()
    return jsonify({"logged_in_as": current_user}), 200
