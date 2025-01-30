from flask import Blueprint, request, jsonify
from utils.db import db
from flask_jwt_extended import jwt_required, get_jwt_identity
from bson import ObjectId

user_bp = Blueprint('users', __name__)


@user_bp.route('/', methods=['GET'])
@jwt_required()
def get_users():
    """
    Retrieves all users.
    """
    current_user = get_jwt_identity()

    if current_user.get('role') != 'admin':
        return jsonify(message="Unauthorized access"), 403

    users = db.users.find()
    users_list = [{"_id": str(user["_id"]), "username": user["username"], "email": user.get("email"),
                   "role": user.get("role", "user")} for user in users]

    return jsonify(users_list), 200


@user_bp.route('/<user_id>', methods=['GET'])
@jwt_required()
def get_user(user_id):
    """
    Retrieves a single user by their ID.
    """
    current_user = get_jwt_identity()

    if current_user.get('role') != 'admin' and str(current_user.get('id')) != user_id:
        return jsonify(message="Unauthorized access"), 403

    user = db.users.find_one({"_id": ObjectId(user_id)})
    if user:
        user_data = {"_id": str(user["_id"]), "username": user["username"], "email": user.get("email"),
                     "role": user.get("role", "user")}
        return jsonify(user_data), 200

    return jsonify(message="User not found"), 404


@user_bp.route('/<user_id>', methods=['PUT'])
@jwt_required()
def update_user(user_id):
    """
    Updates a user's information.
    """
    current_user = get_jwt_identity()
    if current_user.get('role') != 'admin' and str(current_user.get('id')) != user_id:
        return jsonify(message="Unauthorized access"), 403

    data = request.get_json()
    update_data = {}

    if 'username' in data:
        update_data['username'] = data['username']
    if 'password' in data:
        hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
        update_data['password'] = hashed_password
    if 'role' in data and current_user.get('role') == 'admin':
        update_data['role'] = data['role']

    result = db.users.update_one({"_id": ObjectId(user_id)}, {"$set": update_data})
    if result.matched_count:
        return jsonify(message="User updated successfully"), 200

    return jsonify(message="User not found"), 404


@user_bp.route('/<user_id>', methods=['DELETE'])
@jwt_required()
def delete_user(user_id):
    """
    Deletes a user.
    """
    current_user = get_jwt_identity()
    if current_user.get('role') != 'admin':
        return jsonify(message="Unauthorized access"), 403

    result = db.users.delete_one({"_id": ObjectId(user_id)})
    if result.deleted_count:
        return jsonify(message="User deleted successfully"), 200

    return jsonify(message="User not found"), 404
