from flask import request

def serialize_product(product):
    return {
        "_id": str(product["_id"]),
        "name": product["name"],
        "description": product["description"],
        "price": product["price"],
        "category": product["category"],
        "quantity": product["quantity"],
        "image_url": product.get("image_url")
    }

def get_product_data():
    data = request.get_json()
    return {
        "name": data.get('name'),
        "description": data.get('description'),
        "price": data.get('price'),
        "category": data.get('category'),
        "quantity": data.get('quantity'),
        "image_url": data.get('image_url')
    }
