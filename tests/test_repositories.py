import pytest
import json
from unittest.mock import patch, Mock
import subprocess
from src.repositories.requester import RequestRepository


class TestRequestRepository:
    """Test cases for RequestRepository"""

    def test_repository_initialization(self):
        """Test RequestRepository initialization with default timeout"""
        repo = RequestRepository()
        assert repo.timeout == 120

    def test_repository_initialization_custom_timeout(self):
        """Test RequestRepository initialization with custom timeout"""
        repo = RequestRepository(timeout=60)
        assert repo.timeout == 60

    @patch("src.repositories.requester.subprocess.run")
    def test_successful_speedtest_execution(self, mock_run, mock_speedtest_output):
        """Test successful speedtest execution"""
        # Mock successful subprocess result
        mock_result = Mock()
        mock_result.stdout = json.dumps(mock_speedtest_output)
        mock_run.return_value = mock_result

        repo = RequestRepository()
        result = repo.get_speedtest_results()

        mock_run.assert_called_once_with(["speedtest-cli", "--json"], timeout=120)
        assert result == mock_speedtest_output

    @patch("src.repositories.requester.subprocess.run")
    def test_speedtest_timeout_exception(self, mock_run):
        """Test speedtest timeout handling"""
        mock_run.side_effect = subprocess.TimeoutExpired("speedtest-cli", 120)

        repo = RequestRepository()

        with pytest.raises(Exception, match="Speedtest timed out"):
            repo.get_speedtest_results()

    @patch("src.repositories.requester.subprocess.run")
    def test_speedtest_process_error(self, mock_run):
        """Test speedtest process error handling"""
        mock_run.side_effect = subprocess.CalledProcessError(1, "speedtest-cli")

        repo = RequestRepository()

        with pytest.raises(Exception, match="Speedtest failed"):
            repo.get_speedtest_results()

    @patch("src.repositories.requester.subprocess.run")
    def test_speedtest_json_parse_error(self, mock_run):
        """Test handling of invalid JSON response"""
        mock_result = Mock()
        mock_result.stdout = "invalid json"
        mock_run.return_value = mock_result

        repo = RequestRepository()

        with pytest.raises(Exception, match="An error occurred"):
            repo.get_speedtest_results()

    @patch("src.repositories.requester.subprocess.run")
    def test_speedtest_generic_exception(self, mock_run):
        """Test handling of generic exceptions"""
        mock_run.side_effect = RuntimeError("Something went wrong")

        repo = RequestRepository()

        with pytest.raises(Exception, match="An error occurred"):
            repo.get_speedtest_results()

    @patch("src.repositories.requester.subprocess.run")
    def test_custom_timeout_used(self, mock_run, mock_speedtest_output):
        """Test that custom timeout is passed to subprocess"""
        mock_result = Mock()
        mock_result.stdout = json.dumps(mock_speedtest_output)
        mock_run.return_value = mock_result

        repo = RequestRepository(timeout=30)
        repo.get_speedtest_results()

        mock_run.assert_called_once_with(["speedtest-cli", "--json"], timeout=30)
