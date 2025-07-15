from fastapi import status
from fastapi.testclient import TestClient
from src.main import app


class TestMainApp:
    """Test cases for the main FastAPI application"""

    def test_app_initialization(self):
        """Test that the app initializes correctly"""
        assert app is not None
        assert hasattr(app, "routes")

        # Check that routes are registered
        route_paths = [route.path for route in app.routes]
        assert "/" in route_paths
        assert "/speed" in route_paths

    def test_app_with_test_client(self, test_client):
        """Test that test client works with the app"""
        assert isinstance(test_client, TestClient)

    def test_app_route_count(self):
        """Test that the expected number of routes are registered"""
        # FastAPI adds some default routes, so we check for our specific ones
        route_paths = [route.path for route in app.routes]

        # Should have at least our two main routes
        assert "/" in route_paths
        assert "/speed" in route_paths

    def test_app_openapi_schema(self, test_client):
        """Test that OpenAPI schema is available"""
        response = test_client.get("/openapi.json")
        assert response.status_code == status.HTTP_200_OK

        schema = response.json()
        assert "openapi" in schema
        assert "paths" in schema
        assert "/" in schema["paths"]
        assert "/speed" in schema["paths"]

    def test_app_docs_endpoint(self, test_client):
        """Test that API docs endpoint is available"""
        response = test_client.get("/docs")
        assert response.status_code == status.HTTP_200_OK
        assert "text/html" in response.headers["content-type"]

    def test_app_redoc_endpoint(self, test_client):
        """Test that ReDoc endpoint is available"""
        response = test_client.get("/redoc")
        assert response.status_code == status.HTTP_200_OK
        assert "text/html" in response.headers["content-type"]

    def test_app_nonexistent_route(self, test_client):
        """Test accessing a non-existent route returns 404"""
        response = test_client.get("/nonexistent")
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_app_cors_headers(self, test_client):
        """Test basic CORS functionality (if enabled)"""
        response = test_client.get("/")
        # This is just checking the response is successful
        # CORS headers would be added if CORS middleware was configured
        assert response.status_code == status.HTTP_200_OK

    def test_app_health_check_via_root(self, test_client):
        """Test using root endpoint as a health check"""
        response = test_client.get("/")
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == "hiiii :3"

    def test_app_response_headers(self, test_client):
        """Test that responses have expected headers"""
        response = test_client.get("/")
        assert "content-type" in response.headers
        assert "application/json" in response.headers["content-type"]
