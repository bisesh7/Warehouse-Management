class Product:
    def __init__(self, name, description, price, category, quantity, image_url=None):
        self.name = name
        self.description = description
        self.price = price
        self.category = category
        self.quantity = quantity
        self.image_url = image_url
