from api.dependencies.database import SessionLocal
from api.models import model_loader
from api.models.resources import Resource
from api.models.sandwiches import Sandwich
from api.models.recipes import Recipe
from api.models.orders import Order
from api.models.order_details import OrderDetail

def get_or_create(db, model, defaults=None, **lookup):
    obj = db.query(model).filter_by(**lookup).first()
    if obj:
        return obj
    obj = model(**lookup, **(defaults or {}))
    db.add(obj)
    db.flush()
    return obj

def main():
    model_loader.index()
    db = SessionLocal()
    try:
        bread = get_or_create(db, Resource, item="Bread", defaults={"amount": 100})
        ham   = get_or_create(db, Resource, item="Ham", defaults={"amount": 50})
        cheese = get_or_create(db, Resource, item="Cheese", defaults={"amount": 50})

        hc = get_or_create(db, Sandwich, sandwich_name="Ham & Cheese", defaults={"price": 6.50})
        for res, amt in [(bread, 2), (ham, 1), (cheese, 1)]:
            get_or_create(db, Recipe, sandwich_id=hc.id, resource_id=res.id, defaults={"amount": amt})

        order = get_or_create(db, Order, customer_name="Sample Customer",
                              defaults={"description": "Seed order"})
        get_or_create(db, OrderDetail, order_id=order.id, sandwich_id=hc.id, defaults={"amount": 2})

        db.commit()
        print("Seed complete.")
    finally:
        db.close()

if __name__ == "__main__":
    main()

