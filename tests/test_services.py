import pytest

from src.models.speedresponse import SpeedResponse
from src.services.get_speed import SpeedService


class TestSpeedService:
    """Test cases for SpeedService"""

    def test_service_initialization(self, mock_request_repository):
        """Test SpeedService initialization"""
        service = SpeedService(mock_request_repository)
        assert service.request_repository == mock_request_repository

    @pytest.mark.anyio
    async def test_get_speedtest_results_success(
        self, speed_service, mock_request_repository, mock_speedtest_output
    ):
        """Test successful speedtest result processing"""
        mock_request_repository.get_speedtest_results.return_value = (
            mock_speedtest_output
        )

        result = await speed_service.get_speedtest_results()

        assert isinstance(result, SpeedResponse)
        # Convert from bits to megabits (divide by 1,000,000) and round to 2 decimals
        expected_download = round(99478925.14088322 / 1_000_000, 2)  # 99.48
        expected_upload = round(78648744.10145727 / 1_000_000, 2)  # 78.65
        assert result.download_speed == expected_download
        assert result.upload_speed == expected_upload
        assert result.ping == 18.482
        assert result.server_name == "Riga"
        assert result.server_location == "Latvia"
        mock_request_repository.get_speedtest_results.assert_called_once()

    @pytest.mark.anyio
    async def test_get_speedtest_results_with_different_data(
        self, speed_service, mock_request_repository
    ):
        """Test speedtest result processing with different data"""
        test_data = {
            "download": 50000000.0,
            "upload": 25000000.0,
            "ping": 25.5,
            "server": {"name": "Stockholm", "country": "Sweden"},
        }
        mock_request_repository.get_speedtest_results.return_value = test_data

        result = await speed_service.get_speedtest_results()
        expected_download = round(50000000.0 / 1_000_000, 2)  # 50.0
        assert result.download_speed == expected_download
        assert result.server_name == "Stockholm"
        assert result.server_location == "Sweden"

    @pytest.mark.anyio
    async def test_get_speedtest_results_missing_bandwidth_key(
        self, speed_service, mock_request_repository
    ):
        """Test handling of missing download key in response"""
        test_data = {
            # Missing download key entirely
            "upload": 25000000.0,
            "ping": 25.5,
            "server": {"name": "Test Server", "country": "Test Location"},
        }
        mock_request_repository.get_speedtest_results.return_value = test_data

        with pytest.raises(KeyError):
            await speed_service.get_speedtest_results()

    @pytest.mark.anyio
    async def test_get_speedtest_results_missing_server_info(
        self, speed_service, mock_request_repository
    ):
        """Test handling of missing server information"""
        test_data = {
            "download": 50000000.0,
            "upload": 25000000.0,
            "ping": 25.5,
            "server": {},  # Missing name and country
        }
        mock_request_repository.get_speedtest_results.return_value = test_data

        with pytest.raises(KeyError):
            await speed_service.get_speedtest_results()

    @pytest.mark.anyio
    async def test_get_speedtest_results_repository_exception(
        self, speed_service, mock_request_repository
    ):
        """Test handling of repository exceptions"""
        mock_request_repository.get_speedtest_results.side_effect = Exception(
            "Network error"
        )

        with pytest.raises(Exception, match="Network error"):
            await speed_service.get_speedtest_results()

    @pytest.mark.anyio
    async def test_get_speedtest_results_zero_values(
        self, speed_service, mock_request_repository
    ):
        """Test handling of zero speed values"""
        test_data = {
            "download": 0.0,
            "upload": 0.0,
            "ping": 0.0,
            "server": {"name": "No Connection", "country": "Unknown"},
        }
        mock_request_repository.get_speedtest_results.return_value = test_data

        result = await speed_service.get_speedtest_results()

        assert result.download_speed == 0.0
        assert result.upload_speed == 0.0
        assert result.ping == 0.0
