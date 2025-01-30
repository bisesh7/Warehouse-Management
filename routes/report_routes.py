from flask import Blueprint, jsonify, request
from bson import ObjectId
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime
from app import db
from utils.auth import admin_required

report_bp = Blueprint('reports', __name__)

order_collection = db['orders']
user_collection = db['users']
product_collection = db['products']


@report_bp.route('/total_sales', methods=['GET'])
@jwt_required()
@admin_required
def total_sales():
    """
    Calculate and return the total sales.
    """
    print("Debug: Entering total_sales route")
    total_sales = order_collection.aggregate([
        {"$group": {"_id": None, "total_sales": {"$sum": "$total_price"}}}
    ])
    result = list(total_sales)
    total = result[0]['total_sales'] if result else 0
    print(f"Debug: Total sales calculated: {total}")
    return jsonify({"total_sales": total}), 200


@report_bp.route('/orders_by_category', methods=['GET'])
@jwt_required()
@admin_required
def orders_by_category():
    """
    Calculate and return the number of orders by product category.
    """
    print("Debug: Entering orders_by_category route")
    orders_by_category = order_collection.aggregate([
        {"$unwind": "$items"},
        {"$group": {
            "_id": "$items.category",
            "order_count": {"$sum": 1}
        }},
        {"$project": {
            "_id": 0,
            "category": "$_id",
            "order_count": 1
        }}
    ])
    result = list(orders_by_category)
    print(f"Debug: Orders by category calculated: {result}")
    return jsonify({"orders_by_category": result}), 200


@report_bp.route('/inventory_costs', methods=['GET'])
@jwt_required()
@admin_required
def inventory_costs():
    """
    Calculate and return the total inventory costs.
    """
    print("Debug: Entering inventory_costs route")
    inventory_costs = product_collection.aggregate([
        {"$group": {"_id": None, "total_cost": {"$sum": {"$multiply": ["$price", "$quantity"]}}}}
    ])
    result = list(inventory_costs)
    total = result[0]['total_cost'] if result else 0
    print(f"Debug: Total inventory costs calculated: {total}")
    return jsonify({"total_inventory_cost": total}), 200


@report_bp.route('/custom_sales_report', methods=['GET'])
@jwt_required()
@admin_required
def custom_sales_report():
    """
    Generate a customizable sales report based on start and end dates.
    """
    start_date_str = request.args.get('start_date')
    end_date_str = request.args.get('end_date')

    # Validate date inputs
    if not start_date_str or not end_date_str:
        print("Debug: Missing start_date or end_date")
        return jsonify({"message": "Start date and end date are required"}), 400

    try:
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d')
    except (TypeError, ValueError):
        print("Debug: Invalid date format")
        return jsonify({"message": "Invalid date format. Use YYYY-MM-DD."}), 400

    # Debugging: Print the date range
    print(f"Debug: Generating sales report from {start_date} to {end_date}")

    sales_report = order_collection.aggregate([
        {"$match": {"order_date": {"$gte": start_date, "$lt": end_date}}},
        {"$group": {"_id": None, "total_sales": {"$sum": "$total_price"}, "total_orders": {"$sum": 1}}}
    ])
    result = list(sales_report)
    report = result[0] if result else {"total_sales": 0, "total_orders": 0}

    # Debugging: Print the report
    print(f"Debug: Sales report generated: {report}")

    return jsonify(report), 200
