from menu import FoodItem, DrinkItem, Combo
from pricing import PercentageDiscount, FixedAmountDiscount, TaxStrategy, TipStrategy
from inventory import Inventory
from order import Order


def build_system():
    burger = FoodItem(1, "Burger", 8.00, "food")
    fries = FoodItem(2, "Fries", 4.00, "food")
    cola = DrinkItem(3, "Cola", 2.50, "drink")

    combo = Combo(4, "Burger Combo", [burger, cola], 10)

    menu = {
        1: burger,
        2: fries,
        3: cola,
        4: combo
    }

    inventory = Inventory()
    inventory.set_stock(1, 10)
    inventory.set_stock(2, 8)
    inventory.set_stock(3, 20)

    tax_strategy = TaxStrategy({
        "food": 0.06,
        "drink": 0.08,
        "combo": 0.06
    })

    tip_strategy = TipStrategy(15)

    return menu, inventory, tax_strategy, tip_strategy


def list_menu(menu):
    print("\nMENU")
    print("-" * 30)

    for item in menu.values():
        print(item)

    print()


def run_cli():
    menu, inventory, tax_strategy, tip_strategy = build_system()

    order = None
    order_id = 1001

    while True:

        print("====== RESTAURANT SYSTEM ======")
        print("1. Show Menu")
        print("2. Show Inventory")
        print("3. Create Order")
        print("4. Add Item")
        print("5. View Order")
        print("6. Confirm Order")
        print("7. Change Status")
        print("8. Print Receipt")
        print("9. Exit")

        choice = input("Choose option: ")

        if choice == "1":
            list_menu(menu)

        elif choice == "2":
            print("\nINVENTORY")
            print("-" * 30)
            stock = inventory.show_stock()
            for item_id, item in menu.items():
                if item.category != "combo":
                    quantity = stock.get(item_id, 0)
                    print(f"{item.name:20} Stock: {quantity}")

        elif choice == "3":
            order = Order(order_id, tax_strategy, tip_strategy)
            print(f"Order {order_id} created\n")
            order_id += 1

        elif choice == "4":
            if order is None:
                print("Create order first\n")
                continue

            item_id = int(input("Item ID: "))
            qty = int(input("Quantity: "))

            order.add_item(menu[item_id], qty)

        elif choice == "5":
            if order:
                order.view_order()
            else:
                print("No active order\n")

        elif choice == "6":
            order.confirm(inventory)
            print("Order confirmed\n")

        elif choice == "7":
            status = input("Enter next status: ")
            order.change_status(status)

        elif choice == "8":
            print(order.receipt())

        elif choice == "9":
            print("Exiting...")
            break

        else:
            print("Invalid option\n")


if __name__ == "__main__":
    run_cli()