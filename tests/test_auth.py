import pytest
from fastapi.testclient import TestClient
from app.services.auth import auth_service

def test_health_endpoint_no_auth(client: TestClient):
    """Test that health endpoint doesn't require authentication"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

def test_root_endpoint_no_auth(client: TestClient):
    """Test that root endpoint doesn't require authentication"""
    response = client.get("/")
    assert response.status_code == 200
    assert "Savannah Orders API" in response.json()["message"]

def test_create_access_token():
    """Test JWT token creation"""
    data = {"sub": "test_user", "scopes": ["read", "write"]}
    token = auth_service.create_access_token(data)
    assert isinstance(token, str)
    assert len(token) > 0

def test_protected_endpoint_without_token(client: TestClient):
    """Test that protected endpoints require authentication"""
    response = client.get("/api/v1/customers/")
    assert response.status_code == 403  # Changed from 401 to 403

def test_protected_endpoint_with_invalid_token(client: TestClient):
    """Test that invalid tokens are rejected"""
    headers = {"Authorization": "Bearer invalid-token"}
    response = client.get("/api/v1/customers/", headers=headers)
    assert response.status_code == 401

def test_protected_endpoint_with_valid_token(client: TestClient, auth_headers):
    """Test that valid tokens allow access"""
    response = client.get("/api/v1/customers/", headers=auth_headers)
    assert response.status_code == 200
