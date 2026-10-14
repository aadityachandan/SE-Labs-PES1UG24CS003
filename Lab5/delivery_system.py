"""Food delivery order queue manager."""

import json
from datetime import datetime

VALID_STATUSES = ["placed", "cooking", "out_for_delivery", "delivered"]
DEFAULT_MENU = {"pizza": 250, "burger": 150, "fries": 90, "coke": 40}

class OrderQueue:
    """Keeps track of food delivery orders."""

    def __init__(self):
        self.orders = {}
        self.menu = {}
        self.next_id = 1
        self.order_history = []

    def read_menu_config(self, file="menu.json"):
        """Load the menu from a JSON file, or use the default menu."""
        try:
            with open(file, encoding="utf-8") as menu_file:
                self.menu = json.load(menu_file)
        except (OSError, json.JSONDecodeError):
            self.menu = dict(DEFAULT_MENU)

    def create_order(self, customer, items):
        """Create a new order and return its id."""
        if not customer.strip():
            raise ValueError("Customer name is required")
        if not items:
            raise ValueError("An order needs at least one item")
        total = 0
        for item in items:
            if item not in self.menu:
                raise ValueError(f"Unknown dish: {item}. Choose from: {list(self.menu)}")
            total += self.menu[item]
        order_id = self.next_id
        self.orders[order_id] = {
            "customer": customer,
            "items": items,
            "total": total,
            "status": "placed",
        }
        self.order_history.append(order_id)
        self.next_id += 1
        return order_id

    def update_order_status(self, order_id, status):
        """Change the status of an existing order."""
        if status not in VALID_STATUSES:
            raise ValueError(f"Invalid status: {status}")
        if order_id not in self.orders:
            raise KeyError(f"Order not found: {order_id}")
        self.orders[order_id]["status"] = status

    def daily_revenue(self):
        """Return the total of all delivered orders."""
        return sum(
            order["total"]
            for order in self.orders.values()
            if order["status"] == "delivered"
        )

    def backup_orders(self, file="orders.json"):
        """Save all orders to a JSON file."""
        with open(file, "w", encoding="utf-8") as backup_file:
            json.dump(self.orders, backup_file)

    def restore_orders(self, file="orders.json"):
        """Load orders from a JSON file."""
        with open(file, encoding="utf-8") as backup_file:
            data = json.load(backup_file)
        self.orders = {int(key): value for key, value in data.items()}

    def print_queue(self):
        """Print every order in the queue."""
        print(f"Order queue at {datetime.now()}")
        for order_id, order in self.orders.items():
            print(order_id, order["customer"], order["status"],
                  order["total"])

def main():
    """Run a small demo of the order queue."""
    queue = OrderQueue()
    queue.read_menu_config()
    asha_id = queue.create_order("Asha", ["pizza", "coke"])
    ravi_id = queue.create_order("Ravi", ["burger", "fries"])

    bad_orders = [("Meera", ["sushi"]), ("", [])]
    for customer, items in bad_orders:
        try:
            queue.create_order(customer, items)
        except ValueError as error:
            print("Rejected order:", error)

    queue.update_order_status(asha_id, "delivered")
    bad_updates = [(ravi_id, "teleported"), (42, "delivered")]
    for order_id, status in bad_updates:
        try:
            queue.update_order_status(order_id, status)
        except (ValueError, KeyError) as error:
            print("Could not update order:", error)

    print("Revenue today:", queue.daily_revenue())
    queue.backup_orders()
    queue.restore_orders()
    queue.print_queue()

if __name__ == "__main__":
    main()
