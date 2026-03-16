VALID_TRANSITIONS = {
    "Created": "Confirmed",
    "Confirmed": "Preparing",
    "Preparing": "Ready",
    "Ready": "Served",
    "Served": "Paid"
}


class OrderItem:

    def __init__(self, item, quantity):
        self._item = item
        self._quantity = quantity

    @property
    def item(self):
        return self._item

    @property
    def quantity(self):
        return self._quantity

    def increase_quantity(self, amount):
        self._quantity += amount

    def decrease_quantity(self, amount):
        self._quantity -= amount

    def line_subtotal(self):
        return self._item.price * self._quantity

    def __str__(self):
        return f"{self._item.name} x{self._quantity} = ${self.line_subtotal():.2f}"


class Order:

    def __init__(self, order_id, tax_strategy, tip_strategy):
        self._order_id = order_id
        self._items = []
        self._discounts = []
        self._tax_strategy = tax_strategy
        self._tip_strategy = tip_strategy
        self._status = "Created"

    @property
    def status(self):
        return self._status

    def view_order(self):
        print(f"Order ID: {self._order_id}")
        print(f"Status: {self._status}")
        print("-" * 30)

        if not self._items:
            print("Order is empty.")
            return

        for order_item in self._items:
            print(order_item)

        print("-" * 30)
        print(f"Subtotal: ${self.subtotal():.2f}")
        print(f"Discounts: -${self.total_discount():.2f}")
        print(f"After Discount: ${self.discounted_subtotal():.2f}")
        print(f"Tax: ${self.tax():.2f}")
        print(f"Tip: ${self.tip():.2f}")
        print(f"Final Total: ${self.total():.2f}")

    def add_item(self, item, quantity=1):

        if self._status != "Created":
            raise ValueError("Cannot edit order after confirmation")

        for existing in self._items:
            if existing.item.id == item.id:
                existing.increase_quantity(quantity)
                return

        self._items.append(OrderItem(item, quantity))

    def remove_item(self, item_id, quantity=1):

        if self._status != "Created":
            raise ValueError("Cannot edit order after confirmation")

        for order_item in self._items:
            if order_item.item.id == item_id:

                if quantity >= order_item.quantity:
                    self._items.remove(order_item)
                else:
                    order_item.decrease_quantity(quantity)

                return

        raise ValueError("Item not found")

    def add_discount(self, discount):
        self._discounts.append(discount)

    def subtotal(self):
        return sum(item.line_subtotal() for item in self._items)

    def total_discount(self):
        running = self.subtotal()
        total = 0

        for d in self._discounts:
            val = d.apply(running)
            total += val
            running -= val

        return total

    def discounted_subtotal(self):
        return max(0, self.subtotal() - self.total_discount())

    def tax(self):

        raw_tax = self._tax_strategy.calculate_tax(self._items)

        if self.subtotal() == 0:
            return 0

        ratio = self.total_discount() / self.subtotal()

        return raw_tax * (1 - ratio)

    def tip(self):
        base = self.discounted_subtotal() + self.tax()
        return self._tip_strategy.calculate_tip(base)

    def total(self):
        return self.discounted_subtotal() + self.tax() + self.tip()

    def confirm(self, inventory):

        if self._status != "Created":
            raise ValueError("Order already confirmed")

        required = {}

        for order_item in self._items:
            components = order_item.item.get_components()

            for item_id, qty in components.items():
                required[item_id] = required.get(item_id, 0) + qty * order_item.quantity

        for item_id, qty in required.items():

            if not inventory.has_enough(item_id, qty):
                raise ValueError(f"Insufficient stock for item {item_id}")

        for item_id, qty in required.items():
            inventory.reduce_stock(item_id, qty)

        self._status = "Confirmed"

    def change_status(self, new_status):

        if self._status not in VALID_TRANSITIONS:
            raise ValueError("No further transitions allowed")

        expected = VALID_TRANSITIONS[self._status]

        if new_status != expected:
            raise ValueError(f"Invalid transition from {self._status} to {new_status}")

        self._status = new_status

    def receipt(self):

        lines = []
        lines.append("=" * 40)
        lines.append(f"Order ID: {self._order_id}")
        lines.append(f"Status: {self._status}")
        lines.append("-" * 40)

        for item in self._items:
            lines.append(
                f"{item.item.name:20} x{item.quantity:<3} ${item.line_subtotal():>7.2f}"
            )

        lines.append("-" * 40)

        lines.append(f"{'Subtotal':25} ${self.subtotal():>7.2f}")
        lines.append(f"{'Discounts':25} -${self.total_discount():>7.2f}")
        lines.append(f"{'Tax':25} ${self.tax():>7.2f}")
        lines.append(f"{'Tip':25} ${self.tip():>7.2f}")

        lines.append("-" * 40)
        lines.append(f"{'FINAL TOTAL':25} ${self.total():>7.2f}")
        lines.append("=" * 40)

        return "\n".join(lines)