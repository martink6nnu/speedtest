import pytest
from unittest.mock import Mock
from fastapi.testclient import TestClient
from src.main import app
from src.repositories.requester import RequestRepository
from src.services.get_speed import SpeedService


@pytest.fixture
def test_client():
    """FastAPI test client fixture"""
    return TestClient(app)


@pytest.fixture
def mock_speedtest_output():
    """Mock speedtest-cli JSON output matching the user's example"""
    return {
        "download": 99478925.14088322,
        "upload": 78648744.10145727,
        "ping": 18.482,
        "server": {
            "url": "http://speedtest-rix.retn.net:8080/upload.php",
            "lat": "56.9496",
            "lon": "24.1040",
            "name": "Riga",
            "country": "Latvia",
            "cc": "LV",
            "sponsor": "RETN",
            "id": "28935",
            "host": "speedtest-rix.retn.net:8080",
            "d": 279.1799954388942,
            "latency": 18.482
        },
        "timestamp": "2025-07-15T17:49:51.959712Z",
        "bytes_sent": 98418688,
        "bytes_received": 124498202,
        "share": None,
        "client": {
            "ip": "84.50.246.185",
            "lat": "59.4381",
            "lon": "24.7369",
            "isp": "Telia Eesti",
            "isprating": "3.7",
            "rating": "0",
            "ispdlavg": "0",
            "ispulavg": "0",
            "loggedin": "0",
            "country": "EE"
        }
    }


@pytest.fixture
def mock_expected_format():
    """Mock data in the format the current code expects"""
    return {
        "download": {"bandwidth": 99478925.14088322},
        "upload": {"bandwidth": 78648744.10145727},
        "ping": 18.482,
        "server": {
            "name": "Riga",
            "location": "Latvia"
        }
    }


@pytest.fixture
def mock_request_repository():
    """Mock RequestRepository"""
    return Mock(spec=RequestRepository)


@pytest.fixture
def speed_service(mock_request_repository):
    """SpeedService with mocked repository"""
    return SpeedService(mock_request_repository) 