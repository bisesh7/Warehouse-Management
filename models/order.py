class Order:
    def __init__(self, user_id, items, total_price, status="Pending"):
        self.user_id = user_id
        self.items = items
        self.total_price = total_price
        self.status = status

    def to_dict(self):
        return {
            "user_id": self.user_id,
            "items": self.items,
            "total_price": self.total_price,
            "status": self.status,
        }
