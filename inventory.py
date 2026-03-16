class Inventory:
    def __init__(self):
        self._stock = {}

    def set_stock(self, item_id, quantity):
        if quantity < 0:
            raise ValueError("Stock cannot be negative")
        self._stock[item_id] = quantity

    def get_stock(self, item_id):
        return self._stock.get(item_id, 0)

    def has_enough(self, item_id, required_quantity):
        return self.get_stock(item_id) >= required_quantity

    def reduce_stock(self, item_id, quantity):
        if quantity <= 0:
            raise ValueError("Quantity must be greater than 0")

        if not self.has_enough(item_id, quantity):
            raise ValueError(f"Not enough stock for item {item_id}")

        self._stock[item_id] -= quantity

    def show_stock(self):
        return self._stock.copy()