from fastapi.testclient import TestClient
from ..controllers import orders as controller
from ..main import app
import pytest
from ..models import orders as model

# Create a test client for the app
client = TestClient(app)


@pytest.fixture
def db_session(mocker):
    return mocker.Mock()


def test_create_order(db_session):
    # Create a sample order
    order_data = {
        "customer_id": 1,
        "order_type": model.OrderType.takeout,
        "description": "Test order"
    }

    order_object = model.Order(**order_data)

    # Call the create function
    created_order = controller.create(db_session, order_object)

    # Assertions
    assert created_order is not None
    assert created_order.customer_id == 1
    assert created_order.order_type == model.OrderType.takeout
    assert created_order.description == "Test order"

def test_checkout_rejects_expired_promo():
    response = client.post("/orders/checkout", json={
        "name": "ryan",
        "phone": "555-555-5555",
        "address": "123 ABC St",
        "order_type": "takeout",
        "items": [{
            "menu_id": 7,
            "amount": 1
        }],
        "promo_code": "SUMMER15"
    })

    assert response.status_code == 400
    assert "expired" in response.json()["detail"]
