"""Fill the database with demo data for OROS.

Usage (from the repo root):
    python seed.py          # add demo data; safe to run again, nothing is duplicated
    python seed.py --reset  # DROP every table, recreate them, then add demo data

The data is chosen so each required question has something to show:
orders on different days (1.7, 1.8), a nearly-out ingredient (1.2), a rarely
ordered dish and a badly reviewed dish (1.4, 1.5), an active and an expired
promo code (1.6, 2.7), fixed tracking numbers like OROS1001 (2.4), menu
categories (2.5), and takeout/delivery orders (2.3).
"""
import sys
from datetime import datetime
from decimal import Decimal

from api.dependencies.database import Base, SessionLocal, engine
from api.models import model_loader
from api.models.customers import Customer
from api.models.menu import Menu
from api.models.resources import Resource
from api.models.recipes import Recipe
from api.models.promotions import Promotion
from api.models.payments import Payment, PaymentStatus, PaymentType
from api.models.orders import Order, OrderStatus, OrderType
from api.models.order_details import OrderDetail
from api.models.reviews import Review


def get_or_create(db, model, defaults=None, **lookup):
    """Return the row matching `lookup`, creating it (with `defaults`) if missing."""
    obj = db.query(model).filter_by(**lookup).first()
    if obj:
        return obj, False
    obj = model(**lookup, **(defaults or {}))
    db.add(obj)
    db.flush()
    return obj, True


CUSTOMERS = [
    # email (unique lookup), name, phone, address
    ("ana.lopez@example.com", "Ana Lopez", "704-555-0101", "12 Main St, Charlotte, NC"),
    ("ben.park@example.com", "Ben Park", "704-555-0102", "45 Oak Ave, Charlotte, NC"),
    ("chloe.nguyen@example.com", "Chloe Nguyen", "704-555-0103", "9 Elm Ct, Matthews, NC"),
    ("david.okafor@example.com", "David Okafor", "704-555-0104", "300 University Blvd, Charlotte, NC"),
    ("emma.reyes@example.com", "Emma Reyes", "704-555-0105", "77 Pine Rd, Concord, NC"),
]

MENU = [
    # name, description, price, calories, category
    ("Classic Burger", "Beef patty, cheddar, lettuce, tomato on a brioche bun", "10.99", 780, "classic"),
    ("Veggie Burger", "Black bean patty, avocado, lettuce, tomato", "9.99", 620, "vegetarian"),
    ("Spicy Chicken Sandwich", "Crispy chicken, jalapeños, chipotle mayo", "11.49", 850, "spicy"),
    ("Grilled Chicken Salad", "Grilled chicken over greens with light vinaigrette", "10.49", 420, "low fat"),
    ("Margherita Flatbread", "Tomato, mozzarella, basil", "9.49", 690, "vegetarian"),
    ("Kids Chicken Tenders", "Three tenders with a side of fries", "6.99", 540, "kids"),
    ("Fries", "Crispy salted fries", "3.49", 365, "side"),
    ("Lemonade", "Fresh-squeezed lemonade", "2.99", 150, "drink"),
]

RESOURCES = [
    # ingredient, amount in stock, unit
    ("Brioche Bun", 60, "pcs"),
    ("Beef Patty", 40, "pcs"),
    ("Black Bean Patty", 25, "pcs"),
    ("Chicken Breast", 30, "pcs"),
    ("Cheddar", 80, "slice"),
    ("Mozzarella", 3000, "g"),
    ("Lettuce", 2500, "g"),
    ("Tomato", 40, "pcs"),
    ("Avocado", 2, "pcs"),        # nearly out: ordering 3 Veggie Burgers triggers the 1.2 alert
    ("Jalapeños", 800, "g"),
    ("Flatbread Dough", 20, "pcs"),
    ("Potatoes", 15000, "g"),
    ("Lemons", 50, "pcs"),
]

RECIPES = {
    # menu item -> [(ingredient, amount per item)]
    "Classic Burger": [("Brioche Bun", 1), ("Beef Patty", 1), ("Cheddar", 1), ("Lettuce", 20), ("Tomato", 1)],
    "Veggie Burger": [("Brioche Bun", 1), ("Black Bean Patty", 1), ("Avocado", 1), ("Lettuce", 20), ("Tomato", 1)],
    "Spicy Chicken Sandwich": [("Brioche Bun", 1), ("Chicken Breast", 1), ("Jalapeños", 15), ("Lettuce", 15)],
    "Grilled Chicken Salad": [("Chicken Breast", 1), ("Lettuce", 120), ("Tomato", 1)],
    "Margherita Flatbread": [("Flatbread Dough", 1), ("Mozzarella", 120), ("Tomato", 1)],
    "Kids Chicken Tenders": [("Chicken Breast", 1), ("Potatoes", 150)],
    "Fries": [("Potatoes", 200)],
    "Lemonade": [("Lemons", 2)],
}

PROMOTIONS = [
    # code, start, end, discount %
    ("FALL20", datetime(2026, 11, 1), datetime(2026, 12, 31, 23, 59), "20"),
    ("WELCOME10", datetime(2026, 1, 1), datetime(2027, 6, 30, 23, 59), "10"),
    ("SUMMER15", datetime(2026, 6, 1), datetime(2026, 8, 31, 23, 59), "15"),  # expired
]

ORDERS = [
    # tracking #, customer email, date, type, status, promo code, payment (type, status, last4) or None,
    # description, [(menu item, quantity)]
    ("OROS1001", "ana.lopez@example.com", datetime(2026, 11, 20, 12, 15), "takeout", "delivered", None,
     ("credit", "paid", "4242"), "Extra pickles", [("Classic Burger", 2), ("Fries", 2)]),
    ("OROS1002", "ben.park@example.com", datetime(2026, 11, 20, 18, 40), "delivery", "delivered", "FALL20",
     ("debit", "paid", "1881"), None, [("Spicy Chicken Sandwich", 1), ("Lemonade", 1)]),
    ("OROS1003", "chloe.nguyen@example.com", datetime(2026, 11, 21, 13, 5), "takeout", "delivered", None,
     ("credit", "paid", "0005"), None, [("Veggie Burger", 1), ("Grilled Chicken Salad", 1)]),
    ("OROS1004", "david.okafor@example.com", datetime(2026, 11, 22, 19, 30), "delivery", "delivered", "WELCOME10",
     ("credit", "paid", "3434"), "Leave at the door", [("Classic Burger", 3), ("Fries", 3), ("Lemonade", 3)]),
    ("OROS1005", "emma.reyes@example.com", datetime(2026, 11, 22, 12, 0), "takeout", "canceled", None,
     ("debit", "canceled", "7720"), "Customer canceled", [("Kids Chicken Tenders", 2)]),
    ("OROS1006", "ana.lopez@example.com", datetime(2026, 11, 23, 17, 45), "delivery", "delivered", None,
     ("credit", "paid", "4242"), None, [("Spicy Chicken Sandwich", 2), ("Fries", 1)]),
    ("OROS1007", "ben.park@example.com", datetime(2026, 11, 24, 12, 30), "takeout", "ready", "FALL20",
     ("debit", "paid", "1881"), None, [("Classic Burger", 1), ("Kids Chicken Tenders", 1), ("Lemonade", 2)]),
    ("OROS1008", "chloe.nguyen@example.com", datetime(2026, 11, 25, 11, 50), "delivery", "preparing", None,
     ("credit", "paid", "0005"), "No onions", [("Grilled Chicken Salad", 2), ("Lemonade", 1)]),
    ("OROS1009", "emma.reyes@example.com", datetime(2026, 11, 25, 12, 20), "takeout", "pending", None,
     ("credit", "pending", "9911"), None, [("Margherita Flatbread", 1), ("Fries", 1)]),
]

REVIEWS = [
    # customer email, menu item, tracking # (order it came from), score, text
    ("ana.lopez@example.com", "Classic Burger", "OROS1001", 5, "Juicy and perfectly cooked. My go-to order."),
    ("ben.park@example.com", "Spicy Chicken Sandwich", "OROS1002", 4, "Good heat, could use a bit more sauce."),
    ("chloe.nguyen@example.com", "Veggie Burger", "OROS1003", 2, "Patty was dry and fell apart."),
    ("david.okafor@example.com", "Classic Burger", "OROS1004", 5, "Great for a group order, arrived hot."),
    ("ana.lopez@example.com", "Spicy Chicken Sandwich", "OROS1006", 5, "Even better the second time."),
    ("ben.park@example.com", "Kids Chicken Tenders", "OROS1007", 3, "Fine for kids, a little plain."),
    ("chloe.nguyen@example.com", "Grilled Chicken Salad", "OROS1008", 4, "Fresh and light."),
    ("david.okafor@example.com", "Veggie Burger", None, 1, "Way too salty, and the avocado was brown."),
    ("emma.reyes@example.com", "Margherita Flatbread", "OROS1009", 2, "Crust was soggy in the middle."),
]


def seed(db):
    counts = {}

    def note(table, created):
        counts[table] = counts.get(table, 0) + int(created)

    customers = {}
    for email, name, phone, address in CUSTOMERS:
        customers[email], created = get_or_create(
            db, Customer, email=email, defaults={"name": name, "phone": phone, "address": address})
        note("customers", created)

    menu = {}
    for name, description, price, calories, category in MENU:
        menu[name], created = get_or_create(
            db, Menu, name=name,
            defaults={"description": description, "price": Decimal(price), "calories": calories, "category": category})
        note("menu", created)

    resources = {}
    for ingredient, amount, unit in RESOURCES:
        resources[ingredient], created = get_or_create(
            db, Resource, ingredient=ingredient, defaults={"amount": amount, "unit": unit})
        note("resources", created)

    for item, ingredients in RECIPES.items():
        for ingredient, amount in ingredients:
            _, created = get_or_create(
                db, Recipe, menu_id=menu[item].id, resource_id=resources[ingredient].id,
                defaults={"amount": amount})
            note("recipes", created)

    promotions = {}
    for code, start, end, discount in PROMOTIONS:
        promotions[code], created = get_or_create(
            db, Promotion, promo_code=code,
            defaults={"start_date": start, "end_date": end, "discount": Decimal(discount)})
        note("promotions", created)

    orders = {}
    for tracking, email, date, otype, ostatus, promo, payment, description, items in ORDERS:
        subtotal = sum(menu[name].price * qty for name, qty in items)
        discount = promotions[promo].discount if promo else Decimal("0")
        total = (subtotal * (100 - discount) / 100).quantize(Decimal("0.01"))

        order, created = get_or_create(
            db, Order, tracking_number=tracking,
            defaults={
                "customer_id": customers[email].id,
                "order_date": date,
                "order_type": OrderType(otype),
                "status": OrderStatus(ostatus),
                "promotion_id": promotions[promo].id if promo else None,
                "total_price": total,
                "description": description,
            })
        note("orders", created)
        orders[tracking] = order

        for name, qty in items:
            _, created = get_or_create(
                db, OrderDetail, order_id=order.id, menu_id=menu[name].id, defaults={"amount": qty})
            note("order_details", created)

        if payment and order.payment_id is None:
            ptype, pstatus, last4 = payment
            pay = Payment(type=PaymentType(ptype), status=PaymentStatus(pstatus), amount=total,
                          card_number=last4, created_at=date)
            db.add(pay)
            db.flush()
            order.payment_id = pay.id
            note("payments", True)
        else:
            note("payments", False)

    for email, item, tracking, score, text in REVIEWS:
        _, created = get_or_create(
            db, Review, customer_id=customers[email].id, menu_id=menu[item].id,
            order_id=orders[tracking].id if tracking else None,
            defaults={"score": score, "review_text": text})
        note("reviews", created)

    return counts


def main():
    if "--reset" in sys.argv:
        print("Dropping all tables...")
        Base.metadata.drop_all(engine)
    model_loader.index()  # create any missing tables

    db = SessionLocal()
    try:
        counts = seed(db)
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()

    added = ", ".join(f"{table}: {n}" for table, n in counts.items())
    print(f"Seed complete. New rows added -> {added}")


if __name__ == "__main__":
    main()
