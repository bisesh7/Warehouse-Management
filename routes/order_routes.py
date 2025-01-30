from flask import Blueprint, request, jsonify
from bson import ObjectId
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from datetime import datetime
from app import db

order_bp = Blueprint('orders', __name__)

order_collection = db['orders']
cart_collection = db['carts']


@order_bp.route('/checkout', methods=['POST'])
@jwt_required()
def checkout():
    user = get_jwt_identity()
    user_id = user.get('username')  # Assuming the username is used as the user ID
    cart_items = request.json  # Expecting the cart data from the client

    if not cart_items:
        return jsonify({"message": "Cart is empty"}), 400

    order_data = {
        "user_id": user_id,
        "items": cart_items,
        "status": "Pending",
        "total_price": sum(item['price'] * item['quantity'] for item in cart_items),
        "order_date": datetime.utcnow()  # Add the current date and time
    }

    order_id = order_collection.insert_one(order_data).inserted_id

    cart_collection.delete_one({"user_id": user_id, "status": "Pending"})

    return jsonify({"message": "Order placed successfully", "order_id": str(order_id)}), 201


@order_bp.route('/<order_id>', methods=['DELETE'])
@jwt_required()
def delete_order(order_id):
    user = get_jwt_identity()
    user_id = user.get('username')  # Assuming the username is used as the user ID

    order = order_collection.find_one({"_id": ObjectId(order_id), "user_id": user_id})
    if not order:
        return jsonify({"message": "Order not found"}), 404

    order_collection.delete_one({"_id": ObjectId(order_id)})

    return jsonify({"message": "Order deleted successfully"}), 200


@order_bp.route('/', methods=['GET'])
@jwt_required()
def get_orders():
    user = get_jwt_identity()
    user_id = user.get('username')  # Assuming the username is used as the user ID

    orders = order_collection.find({"user_id": user_id})
    orders_list = [{"_id": str(order["_id"]), "items": order["items"], "status": order["status"],
                    "total_price": order["total_price"], "order_date": order.get("order_date")} for order in orders]

    return jsonify(orders_list), 200


@order_bp.route('/all', methods=['GET'])
@jwt_required()
def get_all_orders():
    user = get_jwt_identity()
    raw_jwt = get_jwt()  # Fetch raw JWT for debugging

    # Log the entire JWT payload for debugging
    print(f"JWT Claims: {raw_jwt}")

    # Ensure the user ID is correctly extracted from the sub claim
    username = user.get('username')
    print(f"Username: {username}")  # Logging username for debugging

    # Ensure the user is an admin
    user_doc = db['users'].find_one({"username": username})
    if not user_doc:
        print("User not found")  # Logging for debugging
    elif user_doc['role'] != 'admin':
        print(f"User role: {user_doc['role']} - Access denied")  # Logging user role for debugging
        return jsonify({"message": "Admin access required"}), 403

    # Retrieve all orders from all users
    orders = order_collection.find()
    orders_list = [{"_id": str(order["_id"]), "user_id": order["user_id"], "items": order["items"],
                    "status": order["status"], "total_price": order["total_price"], "order_date": order.get("order_date")} for order in orders]

    return jsonify(orders_list), 200
