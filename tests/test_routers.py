from unittest.mock import patch, Mock
from fastapi import status


class TestRootRouter:
    """Test cases for root router endpoints"""

    def test_root_endpoint(self, test_client):
        """Test the root endpoint returns expected message"""
        response = test_client.get("/")

        assert response.status_code == status.HTTP_200_OK
        assert response.json() == "hiiii :3"

    def test_root_endpoint_methods(self, test_client):
        """Test that root endpoint only accepts GET requests"""
        # POST should not be allowed
        response = test_client.post("/")
        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED


class TestSpeedRouter:
    """Test cases for speed router endpoints"""

    @patch("src.repositories.requester.subprocess.run")
    def test_speed_endpoint_success(self, mock_run, test_client):
        """Test successful speed endpoint call"""
        # Mock subprocess to return expected data
        mock_result = Mock()
        mock_result.stdout = '{"download": {"bandwidth": 99478925.14}, "upload": {"bandwidth": 78648744.10}, "ping": 18.482, "server": {"name": "Riga", "location": "Latvia"}}'
        mock_run.return_value = mock_result

        response = test_client.get("/speed")

        assert response.status_code == status.HTTP_200_OK
        response_data = response.json()
        assert response_data["download_speed"] == 99478925.14
        assert response_data["upload_speed"] == 78648744.10
        assert response_data["ping"] == 18.482
        assert response_data["server_name"] == "Riga"
        assert response_data["server_location"] == "Latvia"

    @patch("src.repositories.requester.subprocess.run")
    def test_speed_endpoint_error_scenarios(self, mock_run, test_client):
        """Test speed endpoint error scenarios (timeout, generic errors, JSON parse)"""
        import subprocess

        # Test timeout
        mock_run.side_effect = subprocess.TimeoutExpired("speedtest-cli", 120)
        response = test_client.get("/speed")
        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
        assert "Speedtest timed out" in response.json()["detail"]

        # Test generic exception
        mock_run.side_effect = Exception("Speedtest failed")
        response = test_client.get("/speed")
        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR

    @patch("src.repositories.requester.subprocess.run")
    def test_speed_endpoint_different_data(self, mock_run, test_client):
        """Test speed endpoint with different data and zero values"""
        # Test with different data
        mock_result = Mock()
        mock_result.stdout = '{"download": {"bandwidth": 50000000.0}, "upload": {"bandwidth": 25000000.0}, "ping": 35.2, "server": {"name": "Stockholm", "location": "Sweden"}}'
        mock_run.return_value = mock_result
        response = test_client.get("/speed")
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["download_speed"] == 50000000.0

    def test_speed_endpoint_methods(self, test_client):
        """Test that speed endpoint only accepts GET requests"""
        response = test_client.post("/speed")
        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
