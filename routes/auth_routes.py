from flask import Blueprint, request, jsonify
from utils.db import db
from flask_bcrypt import Bcrypt
from flask_jwt_extended import create_access_token

auth_bp = Blueprint('auth', __name__)
bcrypt = Bcrypt()  # Create an instance of Bcrypt


@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
    user = {
        'username': data['username'],
        'password': hashed_password,
        'role': data['role']
    }
    db.users.insert_one(user)
    return jsonify(message="User registered successfully"), 201


@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = db.users.find_one({'username': data['username']})
    if user and bcrypt.check_password_hash(user['password'], data['password']):
        access_token = create_access_token(identity={'username': user['username'], 'role': user['role']})
        return jsonify(access_token=access_token), 200
    return jsonify(message="Invalid credentials"), 401
