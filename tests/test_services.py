import pytest
from src.services.get_speed import SpeedService
from src.models.speedresponse import SpeedResponse


class TestSpeedService:
    """Test cases for SpeedService"""

    def test_service_initialization(self, mock_request_repository):
        """Test SpeedService initialization"""
        service = SpeedService(mock_request_repository)
        assert service.request_repository == mock_request_repository

    def test_get_speedtest_results_success(
        self, speed_service, mock_request_repository, mock_expected_format
    ):
        """Test successful speedtest result processing"""
        mock_request_repository.get_speedtest_results.return_value = (
            mock_expected_format
        )

        result = speed_service.get_speedtest_results()

        assert isinstance(result, SpeedResponse)
        assert result.download_speed == 99478925.14088322
        assert result.upload_speed == 78648744.10145727
        assert result.ping == 18.482
        assert result.server_name == "Riga"
        assert result.server_location == "Latvia"
        mock_request_repository.get_speedtest_results.assert_called_once()

    def test_get_speedtest_results_with_different_data(
        self, speed_service, mock_request_repository
    ):
        """Test speedtest result processing with different data"""
        test_data = {
            "download": {"bandwidth": 50000000.0},
            "upload": {"bandwidth": 25000000.0},
            "ping": 25.5,
            "server": {"name": "Stockholm", "location": "Sweden"},
        }
        mock_request_repository.get_speedtest_results.return_value = test_data

        result = speed_service.get_speedtest_results()
        assert result.download_speed == 50000000.0
        assert result.server_name == "Stockholm"

    def test_get_speedtest_results_missing_bandwidth_key(
        self, speed_service, mock_request_repository
    ):
        """Test handling of missing bandwidth key in response"""
        test_data = {
            "download": {},  # Missing bandwidth key
            "upload": {"bandwidth": 25000000.0},
            "ping": 25.5,
            "server": {"name": "Test Server", "location": "Test Location"},
        }
        mock_request_repository.get_speedtest_results.return_value = test_data

        with pytest.raises(KeyError):
            speed_service.get_speedtest_results()

    def test_get_speedtest_results_missing_server_info(
        self, speed_service, mock_request_repository
    ):
        """Test handling of missing server information"""
        test_data = {
            "download": {"bandwidth": 50000000.0},
            "upload": {"bandwidth": 25000000.0},
            "ping": 25.5,
            "server": {},  # Missing name and location
        }
        mock_request_repository.get_speedtest_results.return_value = test_data

        with pytest.raises(KeyError):
            speed_service.get_speedtest_results()

    def test_get_speedtest_results_repository_exception(
        self, speed_service, mock_request_repository
    ):
        """Test handling of repository exceptions"""
        mock_request_repository.get_speedtest_results.side_effect = Exception(
            "Network error"
        )

        with pytest.raises(Exception, match="Network error"):
            speed_service.get_speedtest_results()

    def test_get_speedtest_results_zero_values(
        self, speed_service, mock_request_repository
    ):
        """Test handling of zero speed values"""
        test_data = {
            "download": {"bandwidth": 0.0},
            "upload": {"bandwidth": 0.0},
            "ping": 0.0,
            "server": {"name": "No Connection", "location": "Unknown"},
        }
        mock_request_repository.get_speedtest_results.return_value = test_data

        result = speed_service.get_speedtest_results()

        assert result.download_speed == 0.0
        assert result.upload_speed == 0.0
        assert result.ping == 0.0
