from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required
from utils.db import db
from utils.auth import admin_required
from utils.helpers import serialize_product, get_product_data
from bson import ObjectId

product_bp = Blueprint('products', __name__)


# Create a new product (Admin only)
@product_bp.route('/add', methods=['POST'])
@jwt_required()
@admin_required
def add_product():
    product = get_product_data()
    db.products.insert_one(product)
    return jsonify(message="Product added successfully"), 201


# Get all products
@product_bp.route('/', methods=['GET'])
def get_products():
    products = db.products.find()
    return jsonify([serialize_product(product) for product in products]), 200


# Get a specific product by ID
@product_bp.route('/<product_id>', methods=['GET'])
def get_product(product_id):
    product = db.products.find_one({"_id": ObjectId(product_id)})
    if product:
        return jsonify(serialize_product(product)), 200
    return jsonify(message="Product not found"), 404


# Update a product (Admin only)
@product_bp.route('/update/<product_id>', methods=['PUT'])
@jwt_required()
@admin_required
def update_product(product_id):
    updated_product = get_product_data()
    result = db.products.update_one({"_id": ObjectId(product_id)}, {"$set": updated_product})
    if result.matched_count:
        return jsonify(message="Product updated successfully"), 200
    return jsonify(message="Product not found"), 404


# Delete a product (Admin only)
@product_bp.route('/delete/<product_id>', methods=['DELETE'])
@jwt_required()
@admin_required
def delete_product(product_id):
    result = db.products.delete_one({"_id": ObjectId(product_id)})
    if result.deleted_count:
        return jsonify(message="Product deleted successfully"), 200
    return jsonify(message="Product not found"), 404
