from . import orders, order_details, recipes, sandwiches, resources, customers, promotions, payments, reviews

from ..dependencies.database import engine


def index():
    # All models share one Base, so a single create_all builds every table
    # in foreign-key order.
    orders.Base.metadata.create_all(engine)
