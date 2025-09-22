import pytest
from fastapi.testclient import TestClient

def test_create_customer(client: TestClient, auth_headers):
    customer_data = {
        "name": "John Doe",
        "code": "CUST001",
        "phone_number": "+254700123456",
        "email": "john@example.com"
    }
    
    response = client.post("/api/v1/customers/", json=customer_data, headers=auth_headers)
    assert response.status_code == 201
    
    data = response.json()
    assert data["name"] == customer_data["name"]
    assert data["code"] == customer_data["code"]
    assert "id" in data
    assert "created_at" in data

def test_create_customer_duplicate_code(client: TestClient, auth_headers):
    customer_data = {
        "name": "John Doe",
        "code": "CUST001",
        "phone_number": "+254700123456"
    }
    
    # Create first customer
    client.post("/api/v1/customers/", json=customer_data, headers=auth_headers)
    
    # Try to create duplicate
    response = client.post("/api/v1/customers/", json=customer_data, headers=auth_headers)
    assert response.status_code == 400
    assert "already exists" in response.json()["detail"]

def test_get_customers(client: TestClient, auth_headers):
    # Create a customer first
    customer_data = {
        "name": "Jane Doe",
        "code": "CUST002",
        "phone_number": "+254700123457"
    }
    client.post("/api/v1/customers/", json=customer_data, headers=auth_headers)
    
    response = client.get("/api/v1/customers/", headers=auth_headers)
    assert response.status_code == 200
    
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1

def test_get_customer_by_id(client: TestClient, auth_headers):
    # Create a customer first
    customer_data = {
        "name": "Jane Smith",
        "code": "CUST003",
        "phone_number": "+254700123458"
    }
    create_response = client.post("/api/v1/customers/", json=customer_data, headers=auth_headers)
    customer_id = create_response.json()["id"]
    
    response = client.get(f"/api/v1/customers/{customer_id}", headers=auth_headers)
    assert response.status_code == 200
    
    data = response.json()
    assert data["name"] == customer_data["name"]
    assert data["id"] == customer_id

def test_update_customer(client: TestClient, auth_headers):
    # Create a customer first
    customer_data = {
        "name": "Bob Johnson",
        "code": "CUST004",
        "phone_number": "+254700123459"
    }
    create_response = client.post("/api/v1/customers/", json=customer_data, headers=auth_headers)
    customer_id = create_response.json()["id"]
    
    # Update customer
    update_data = {"phone_number": "+254700987654"}
    response = client.put(f"/api/v1/customers/{customer_id}", json=update_data, headers=auth_headers)
    assert response.status_code == 200
    
    data = response.json()
    assert data["phone_number"] == update_data["phone_number"]
    assert data["name"] == customer_data["name"]  # Should remain unchanged

def test_delete_customer(client: TestClient, auth_headers):
    # Create a customer first
    customer_data = {
        "name": "Alice Brown",
        "code": "CUST005",
        "phone_number": "+254700123460"
    }
    create_response = client.post("/api/v1/customers/", json=customer_data, headers=auth_headers)
    customer_id = create_response.json()["id"]
    
    # Delete customer
    response = client.delete(f"/api/v1/customers/{customer_id}", headers=auth_headers)
    assert response.status_code == 200
    assert "deleted successfully" in response.json()["message"]
    
    # Verify customer is deleted
    get_response = client.get(f"/api/v1/customers/{customer_id}", headers=auth_headers)
    assert get_response.status_code == 404

def test_unauthorized_access(client: TestClient):
    response = client.get("/api/v1/customers/")
    assert response.status_code == 403  # Changed from 401 to 403
