from flask import jsonify
from flask_jwt_extended import get_jwt_identity
from functools import wraps

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user = get_jwt_identity()
        if user['role'] != 'admin':
            return jsonify(message="Admin access required"), 403
        return f(*args, **kwargs)
    return decorated_function
