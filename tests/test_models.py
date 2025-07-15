import pytest
from pydantic import ValidationError
from src.models.speedresponse import SpeedResponse


class TestSpeedResponse:
    """Test cases for SpeedResponse model"""

    def test_valid_speed_response_creation(self):
        """Test creating a valid SpeedResponse instance"""
        response = SpeedResponse(
            download_speed=99478925.14,
            upload_speed=78648744.10,
            ping=18.482,
            server_name="Riga",
            server_location="Latvia"
        )
        
        assert response.download_speed == 99478925.14
        assert response.upload_speed == 78648744.10
        assert response.ping == 18.482
        assert response.server_name == "Riga"
        assert response.server_location == "Latvia"

    def test_speed_response_dict_conversion(self):
        """Test converting SpeedResponse to dictionary"""
        response = SpeedResponse(
            download_speed=100.5,
            upload_speed=50.25,
            ping=10.0,
            server_name="Test Server",
            server_location="Test Location"
        )
        
        expected_dict = {
            "download_speed": 100.5,
            "upload_speed": 50.25,
            "ping": 10.0,
            "server_name": "Test Server",
            "server_location": "Test Location"
        }
        
        assert response.model_dump() == expected_dict

    def test_speed_response_missing_fields(self):
        """Test SpeedResponse with missing required fields"""
        with pytest.raises(ValidationError):
            SpeedResponse(
                download_speed=100.0,
                upload_speed=50.0
                # Missing ping, server_name, server_location
            )

    def test_speed_response_invalid_types(self):
        """Test SpeedResponse with invalid field types"""
        with pytest.raises(ValidationError):
            SpeedResponse(
                download_speed="not_a_number",
                upload_speed=50.0,
                ping=10.0,
                server_name="Test",
                server_location="Location"
            )

    def test_speed_response_negative_values(self):
        """Test SpeedResponse accepts negative values (edge case)"""
        response = SpeedResponse(
            download_speed=-1.0,
            upload_speed=-1.0,
            ping=-1.0,
            server_name="Error Server",
            server_location="Error Location"
        )
        
        assert response.download_speed == -1.0
        assert response.upload_speed == -1.0
        assert response.ping == -1.0

    def test_speed_response_zero_values(self):
        """Test SpeedResponse with zero values"""
        response = SpeedResponse(
            download_speed=0.0,
            upload_speed=0.0,
            ping=0.0,
            server_name="",
            server_location=""
        )
        
        assert response.download_speed == 0.0
        assert response.upload_speed == 0.0
        assert response.ping == 0.0
        assert response.server_name == ""
        assert response.server_location == "" 