import random
import fastapi
from fastapi.testclient import TestClient
from main import app
from app import models

TEST_USERNAME = "damian"
TEST_PASSWORD = "test"
TEST_EMAIL = "test@example.com"


class TestCredentials:
    def __init__(self, username: str, password: str, email: str):
        self.username = username
        self.password = password
        self.email = email


class PaperhandsTestClient(TestClient):
    def __init__(self, app: fastapi.FastAPI, credentials: TestCredentials):
        self.client = TestClient(app)
        self.credentials = credentials
        self.access_token = None
        self.portfolio: models.Portfolio = None
        self.order_details = {
            "symbol": "AAPL",
            "quantity": 10,
            "side": "BUY",
            "order_type": "LMT",
            "limit_price": 150.0,
        }
        self.order_response_id = None

    def test_create_user(self):
        form_data = {
            "email": self.credentials.email,
            "username": self.credentials.username + str(random.randint(1, 1000)),
            "password": self.credentials.password,
        }
        response = self.client.post("/signup", data=form_data)
        assert response.status_code == 201

    def test_create_user_exists(self):
        form_data = {
            "email": self.credentials.email,
            "username": self.credentials.username,
            "password": self.credentials.password,
        }
        response = self.client.post("/signup", data=form_data)
        assert response.status_code == 400
        assert response.json()["detail"] == "Username already exists"

    def test_login_for_access_token(self):
        form_data = {
            "username": self.credentials.username,
            "password": self.credentials.password,
        }
        response = self.client.post("/token", data=form_data)
        assert response.status_code == 200
        assert response.json()["token_type"] == "bearer"
        assert "access_token" in response.json()
        assert "access_token_expires" in response.json()
        self.access_token = response.json()["access_token"]

    def test_refresh_access_token(self):
        response = self.client.post(
            "/token/refresh", headers={"Authorization": f"Bearer {self.access_token}"}
        )
        assert response.status_code == 200
        assert response.json()["token_type"] == "bearer"
        assert "access_token" in response.json()
        assert "access_token_expires" in response.json()

    def test_refresh_access_token_invalid_token(self):
        # We can use this method to proxy test the get_current_user method, since
        # if the token is invalid, the user will be None.
        access_token = "invalid_token"
        response = self.client.post(
            "/token/refresh", headers={"Authorization": f"Bearer {access_token}"}
        )
        assert response.status_code == 401
        assert response.json()["detail"] == "Could not validate credentials"

    def test_read_users_me(self):
        response = self.client.get(
            "/users/me", headers={"Authorization": f"Bearer {self.access_token}"}
        )
        assert response.status_code == 200
        assert response.json() is not None

    def test_create_portfolio(self):
        form_data = {"portfolio_name": "My Portfolio", "is_public": True}
        response = self.client.post(
            "/portfolio",
            data=form_data,
            headers={"Authorization": f"Bearer {self.access_token}"},
        )
        assert response.status_code == 200
        assert response.json() is not None
        self.portfolio = models.Portfolio(**response.json())
        assert self.portfolio.name == "My Portfolio"
        assert self.portfolio.is_public == True
        assert self.portfolio.owner_id is not None
        assert self.portfolio.id is not None
        assert self.portfolio.orders == []
        assert self.portfolio.positions == []

    def test_get_portfolio(self):
        response = self.client.get(
            f"/portfolio",
            params={"id": self.portfolio.id},
            headers={"Authorization": f"Bearer {self.access_token}"},
        )
        assert response.status_code == 200
        assert response.json() is not None
        portfolio = models.Portfolio(**response.json())
        assert portfolio.name == "My Portfolio"
        assert portfolio.is_public == True
        assert portfolio.owner_id is not None
        assert portfolio.id is not None

    def test_delete_portfolio(self):
        response = self.client.delete(
            f"/portfolio?id={self.portfolio.id}",
            headers={"Authorization": f"Bearer {self.access_token}"},
        )
        assert response.status_code == 204

    def test_update_portfolio(self):
        form_data = {"portfolio_name": "Updated Portfolio", "is_public": True}
        response = self.client.put(
            f"/portfolio?id={self.portfolio.id}",
            data=form_data,
            headers={"Authorization": f"Bearer {self.access_token}"},
        )
        assert response.status_code == 200
        assert response.json() is not None

    def test_create_order(self):
        response = self.client.post(
            f"/order?id={self.portfolio.id}",
            data=self.order_details,
            headers={"Authorization": f"Bearer {self.access_token}"},
        )
        assert response.status_code == 200
        assert response.json() is not None
        self.order_response = models.Order(**response.json())
        assert self.order_response.symbol == self.order_details["symbol"]
        assert self.order_response.quantity == self.order_details["quantity"]
        assert self.order_response.side == self.order_details["side"]
        assert self.order_response.order_type == self.order_details["order_type"]
        assert self.order_response.limit_price == self.order_details["limit_price"]
        assert self.order_response.portfolio_id == self.portfolio.id
        assert self.order_response.id is not None
        self.order_response_id = self.order_response.id
        response = self.client.get(
            f"/portfolio",
            params={"id": self.portfolio.id},
            headers={"Authorization": f"Bearer {self.access_token}"},
        )
        assert response.status_code == 200
        assert response.json() is not None
        portfolio = models.Portfolio(**response.json())
        assert portfolio.orders is not None
        assert len(portfolio.orders) == 1
        assert portfolio.orders[0].id == self.order_response.id

    def test_get_order(self):
        response = self.client.get(
            f"/order?id={self.order_response_id}",
            headers={"Authorization": f"Bearer {self.access_token}"},
        )
        assert response.status_code == 200
        assert response.json() is not None
        order_response = models.Order(**response.json())
        assert order_response.symbol == self.order_details["symbol"]
        assert order_response.quantity == self.order_details["quantity"]
        assert order_response.side == self.order_details["side"]
        assert order_response.order_type == self.order_details["order_type"]
        assert order_response.limit_price == self.order_details["limit_price"]
        assert order_response.portfolio_id == self.portfolio.id
        assert order_response.id is not None

    def test_delete_order(self):
        response = self.client.delete(
            f"/order?id={self.order_response_id}",
            headers={"Authorization": f"Bearer {self.access_token}"},
        )
        assert response.status_code == 204

    def test_get_symbols(self):
        response = self.client.get(
            f"/symbols",
            headers={"Authorization": f"Bearer {self.access_token}"},
        )
        assert response.status_code == 200
        assert response.json() is not None
        assert len(response.json()) > 0

    def test_get_hmds(self, symbol="AAPL"):
        response = self.client.get(
            f"/symbols/hmds",
            params={"symbol": symbol},
            headers={"Authorization": f"Bearer {self.access_token}"},
        )
        assert response.status_code == 200
        assert response.json() is not None
        assert len(response.json()) > 0

if __name__ == "__main__":
    test_credentials = TestCredentials(TEST_USERNAME, TEST_PASSWORD, TEST_EMAIL)
    test_client = PaperhandsTestClient(app, test_credentials)
    test_client.test_create_user()
    test_client.test_login_for_access_token()
    test_client.test_read_users_me()
    test_client.test_create_portfolio()
    test_client.test_get_portfolio()
    test_client.test_update_portfolio()
    test_client.test_create_order()
    test_client.test_get_order()
    test_client.test_delete_order()
    test_client.test_get_symbols()
    test_client.test_get_hmds("AAPL")
    test_client.test_delete_portfolio()
