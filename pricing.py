from abc import ABC, abstractmethod


class Discount(ABC):
    def __init__(self, name):
        self._name = name

    @property
    def name(self):
        return self._name

    @abstractmethod
    def apply(self, amount):
        pass


class PercentageDiscount(Discount):
    def __init__(self, name, percent):
        super().__init__(name)
        self._percent = percent

    @property
    def percent(self):
        return self._percent

    def apply(self, amount):
        return amount * (self._percent / 100)


class FixedAmountDiscount(Discount):
    def __init__(self, name, discount_amount):
        super().__init__(name)
        self._discount_amount = discount_amount

    @property
    def discount_amount(self):
        return self._discount_amount

    def apply(self, amount):
        return min(self._discount_amount, amount)

class TaxStrategy:
    def __init__(self, rates):
        self._rates = rates

    @property
    def rates(self):
        return self._rates.copy()

    def calculate_tax(self, order_items):
        total_tax = 0

        for order_item in order_items:
            category = order_item.item.category
            rate = self._rates.get(category, 0)
            total_tax += order_item.line_subtotal() * rate

        return total_tax


class TipStrategy:
    def __init__(self, tip_percent):
        self._tip_percent = tip_percent

    @property
    def tip_percent(self):
        return self._tip_percent

    def calculate_tip(self, amount):
        return amount * (self._tip_percent / 100)