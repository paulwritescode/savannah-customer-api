import pytest
from fastapi.testclient import TestClient
from datetime import datetime

def test_create_order(client: TestClient, auth_headers):
    # First create a customer
    customer_data = {
        "name": "Test Customer",
        "code": "CUST006",
        "phone_number": "+254700123461"
    }
    customer_response = client.post("/api/v1/customers/", json=customer_data, headers=auth_headers)
    customer_id = customer_response.json()["id"]
    
    # Create order
    order_data = {
        "customer_id": customer_id,
        "item": "Laptop",
        "amount": 50000.00,
        "time": datetime.now().isoformat(),
        "description": "High-end laptop for business use"
    }
    
    response = client.post("/api/v1/orders/", json=order_data, headers=auth_headers)
    assert response.status_code == 201
    
    data = response.json()
    assert data["item"] == order_data["item"]
    assert float(data["amount"]) == order_data["amount"]
    assert data["customer_id"] == customer_id

def test_create_order_invalid_customer(client: TestClient, auth_headers):
    order_data = {
        "customer_id": "550e8400-e29b-41d4-a716-446655440000",  # Non-existent UUID
        "item": "Phone",
        "amount": 25000.00,
        "time": datetime.now().isoformat(),
        "description": "Smartphone for personal use"
    }
    
    response = client.post("/api/v1/orders/", json=order_data, headers=auth_headers)
    assert response.status_code == 404
    assert "Customer not found" in response.json()["detail"]

def test_get_orders(client: TestClient, auth_headers):
    response = client.get("/api/v1/orders/", headers=auth_headers)
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_orders_by_customer(client: TestClient, auth_headers):
    # Create a customer and order
    customer_data = {
        "name": "Order Test Customer",
        "code": "CUST007",
        "phone_number": "+254700123462"
    }
    customer_response = client.post("/api/v1/customers/", json=customer_data, headers=auth_headers)
    customer_id = customer_response.json()["id"]
    
    order_data = {
        "customer_id": customer_id,
        "item": "Tablet",
        "amount": 30000.00,
        "time": datetime.now().isoformat(),
        "description": "Tablet for entertainment"
    }
    client.post("/api/v1/orders/", json=order_data, headers=auth_headers)
    
    # Get orders for specific customer
    response = client.get(f"/api/v1/orders/?customer_id={customer_id}", headers=auth_headers)
    assert response.status_code == 200
    
    data = response.json()
    assert isinstance(data, list)
    assert all(order["customer_id"] == customer_id for order in data)

def test_get_order_by_id(client: TestClient, auth_headers):
    # Create a customer and order
    customer_data = {
        "name": "Single Order Customer",
        "code": "CUST008",
        "phone_number": "+254700123463"
    }
    customer_response = client.post("/api/v1/customers/", json=customer_data, headers=auth_headers)
    customer_id = customer_response.json()["id"]
    
    order_data = {
        "customer_id": customer_id,
        "item": "Smartphone",
        "amount": 40000.00,
        "time": datetime.now().isoformat(),
        "description": "Latest smartphone model"
    }
    order_response = client.post("/api/v1/orders/", json=order_data, headers=auth_headers)
    order_id = order_response.json()["id"]
    
    # Get order by ID
    response = client.get(f"/api/v1/orders/{order_id}", headers=auth_headers)
    assert response.status_code == 200
    
    data = response.json()
    assert data["item"] == order_data["item"]
    assert data["id"] == order_id

def test_update_order(client: TestClient, auth_headers):
    # Create a customer and order
    customer_data = {
        "name": "Update Order Customer",
        "code": "CUST009",
        "phone_number": "+254700123464"
    }
    customer_response = client.post("/api/v1/customers/", json=customer_data, headers=auth_headers)
    customer_id = customer_response.json()["id"]
    
    order_data = {
        "customer_id": customer_id,
        "item": "Old Item",
        "amount": 10000.00,
        "time": datetime.now().isoformat(),
        "description": "Old item description"
    }
    order_response = client.post("/api/v1/orders/", json=order_data, headers=auth_headers)
    order_id = order_response.json()["id"]
    
    # Update order
    update_data = {"item": "New Item", "amount": 15000.00}
    response = client.put(f"/api/v1/orders/{order_id}", json=update_data, headers=auth_headers)
    assert response.status_code == 200
    
    data = response.json()
    assert data["item"] == update_data["item"]
    assert float(data["amount"]) == update_data["amount"]

def test_delete_order(client: TestClient, auth_headers):
    # Create a customer and order
    customer_data = {
        "name": "Delete Order Customer",
        "code": "CUST010",
        "phone_number": "+254700123465"
    }
    customer_response = client.post("/api/v1/customers/", json=customer_data, headers=auth_headers)
    customer_id = customer_response.json()["id"]
    
    order_data = {
        "customer_id": customer_id,
        "item": "To Delete",
        "amount": 5000.00,
        "time": datetime.now().isoformat(),
        "description": "Item to be deleted"
    }
    order_response = client.post("/api/v1/orders/", json=order_data, headers=auth_headers)
    order_id = order_response.json()["id"]
    
    # Delete order
    response = client.delete(f"/api/v1/orders/{order_id}", headers=auth_headers)
    assert response.status_code == 200
    assert "deleted successfully" in response.json()["message"]
    
    # Verify order is deleted
    get_response = client.get(f"/api/v1/orders/{order_id}", headers=auth_headers)
    assert get_response.status_code == 404
