import pytest
import app.main as main
from app.models.stock import Stock
import app.routers.router_orders as orders
import app.routers.router_players as players
from fastapi.testclient import TestClient
from app.models.order_book import OrderBook


@pytest.fixture(scope="function")
def client():
    main.get_config = lambda: {
        "testing": True,
    }
    app = main.app
    new_stock = Stock()
    orders.stock = new_stock
    players.stock = new_stock
    client_api_v1 = TestClient(app)
    yield client_api_v1


@pytest.fixture(scope="function")
def stock():
    new_stock = Stock()
    yield new_stock
