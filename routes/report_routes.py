from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from utils.db import db
from datetime import datetime

report_bp = Blueprint('reports', __name__)


# Sales report (Admin only)
@report_bp.route('/sales', methods=['GET'])
@jwt_required()
def sales_report():
    user = get_jwt_identity()
    if user['role'] != 'admin':
        return jsonify(message="Admin access required"), 403

    sales = db.transactions.aggregate([
        {"$group": {"_id": None, "total_sales": {"$sum": "$total"}, "total_items_sold": {"$sum": "$quantity"}}}
    ])
    result = list(sales)
    if result:
        return jsonify(result[0]), 200
    return jsonify(message="No sales data found"), 404


# Inventory cost report (Admin only)
@report_bp.route('/inventory', methods=['GET'])
@jwt_required()
def inventory_report():
    user = get_jwt_identity()
    if user['role'] != 'admin':
        return jsonify(message="Admin access required"), 403

    products = db.products.find()
    total_inventory_cost = sum([product['price'] * product['quantity'] for product in products])
    return jsonify(total_inventory_cost=total_inventory_cost), 200


# Custom report by date range (Admin only)
@report_bp.route('/sales_by_date', methods=['POST'])
@jwt_required()
def sales_by_date():
    user = get_jwt_identity()
    if user['role'] != 'admin':
        return jsonify(message="Admin access required"), 403

    data = request.get_json()
    start_date = datetime.strptime(data['start_date'], '%Y-%m-%d')
    end_date = datetime.strptime(data['end_date'], '%Y-%m-%d')

    sales = db.transactions.aggregate([
        {"$match": {"date": {"$gte": start_date, "$lte": end_date}}},
        {"$group": {"_id": None, "total_sales": {"$sum": "$total"}, "total_items_sold": {"$sum": "$quantity"}}}
    ])
    result = list(sales)
    if result:
        return jsonify(result[0]), 200
    return jsonify(message="No sales data found for the specified period"), 404
