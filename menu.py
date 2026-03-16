
class MenuItem():
    def __init__(self, id, name, price, category, available=True):
        self._id = id
        self._name = name
        self._price = price
        self._category = category
        self._available = available

    @property
    def id(self):
        return self._id
    @property
    def name(self):
        return self._name
    @property
    def price(self):
        return self._price
    @property
    def category(self):
        return self._category
    @property
    def available(self):
        return self._available

    def setAvailability(self, value):
        self._available = value

    def __str__(self):
        status = "Available" if self.available else "Unavailable"
        return f"{self._id} | {self._name} | {self._category} | {self._price} | {status}"

    def get_components(self):
        return {self.id: 1}

class FoodItem(MenuItem):
    pass

class DrinkItem(MenuItem):
    pass

class Combo(MenuItem):
    def __init__(self, id, name, items, discount_percent=10, available=True):
        super().__init__(id, name, 0, "combo", available)
        self._items = items
        self._discount_percent = discount_percent

    def get_price(self):
        total = sum(item.price for item in self._items)
        discount = total * (self._discount_percent / 100)
        return total - discount

    @property
    def price(self):
        return self.get_price()
    @property
    def items(self):
        return self._items

    def __str__(self):
        names = ", ".join(item.name for item in self._items)
        return f"{self.id} | {self.name} | Combo[{names}] | ${self.price:.2f}"

    def get_components(self):
        components = {}
        for item in self._items:
            inner_components = item.get_components()
            for item_id, qty in inner_components.items():
                components[item_id] = components.get(item_id, 0) + qty
        return components

