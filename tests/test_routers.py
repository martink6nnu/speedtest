from unittest.mock import patch, Mock
from fastapi import status
import json
import asyncio


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

    @patch("src.repositories.requester.asyncio.create_subprocess_exec")
    @patch("src.repositories.requester.asyncio.wait_for")
    def test_speed_endpoint_success(
        self, mock_wait_for, mock_create_subprocess, test_client
    ):
        """Test successful speed endpoint call"""
        # Mock subprocess to return expected data in real speedtest-cli format
        speedtest_data = {
            "download": 99478925.14,
            "upload": 78648744.10,
            "ping": 18.482,
            "server": {"name": "Riga", "country": "Latvia"},
        }

        mock_process = Mock()
        mock_stdout = json.dumps(speedtest_data).encode()
        mock_stderr = b""
        mock_wait_for.return_value = (mock_stdout, mock_stderr)
        mock_create_subprocess.return_value = mock_process

        response = test_client.get("/speed")

        assert response.status_code == status.HTTP_200_OK
        response_data = response.json()
        # Values should be converted from bits to megabits and rounded to 2 decimals
        assert response_data["download_speed"] == round(
            99478925.14 / 1_000_000, 2
        )  # 99.48
        assert response_data["upload_speed"] == round(
            78648744.10 / 1_000_000, 2
        )  # 78.65
        assert response_data["ping"] == 18.482
        assert response_data["server_name"] == "Riga"
        assert response_data["server_location"] == "Latvia"

    @patch("src.repositories.requester.asyncio.create_subprocess_exec")
    @patch("src.repositories.requester.asyncio.wait_for")
    def test_speed_endpoint_error_scenarios(
        self, mock_wait_for, mock_create_subprocess, test_client
    ):
        """Test speed endpoint error scenarios (timeout, generic errors, JSON parse)"""
        import subprocess

        # Test timeout
        mock_process = Mock()
        mock_create_subprocess.return_value = mock_process
        mock_wait_for.side_effect = asyncio.TimeoutError()
        response = test_client.get("/speed")
        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
        assert "Speedtest timed out" in response.json()["detail"]

        # Test generic exception
        mock_wait_for.side_effect = Exception("Network error")
        response = test_client.get("/speed")
        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR

    @patch("src.repositories.requester.asyncio.create_subprocess_exec")
    @patch("src.repositories.requester.asyncio.wait_for")
    def test_speed_endpoint_different_data(
        self, mock_wait_for, mock_create_subprocess, test_client
    ):
        """Test speed endpoint with different data and zero values"""
        # Test with different data
        speedtest_data = {
            "download": 50000000.0,
            "upload": 25000000.0,
            "ping": 35.2,
            "server": {"name": "Stockholm", "country": "Sweden"},
        }

        mock_process = Mock()
        mock_stdout = json.dumps(speedtest_data).encode()
        mock_stderr = b""
        mock_wait_for.return_value = (mock_stdout, mock_stderr)
        mock_create_subprocess.return_value = mock_process

        response = test_client.get("/speed")
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["download_speed"] == round(
            50000000.0 / 1_000_000, 2
        )  # 50.0

    def test_speed_endpoint_methods(self, test_client):
        """Test that speed endpoint only accepts GET requests"""
        response = test_client.post("/speed")
        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
