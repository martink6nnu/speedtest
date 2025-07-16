import pytest
import json
from unittest.mock import patch, Mock
import subprocess
import asyncio
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

    @pytest.mark.anyio
    @patch("src.repositories.requester.asyncio.create_subprocess_exec")
    @patch("src.repositories.requester.asyncio.wait_for")
    async def test_successful_speedtest_execution(
        self, mock_wait_for, mock_create_subprocess, mock_speedtest_output
    ):
        """Test successful speedtest execution"""
        # Mock successful subprocess result
        mock_process = Mock()
        mock_stdout = json.dumps(mock_speedtest_output).encode()
        mock_stderr = b""
        mock_wait_for.return_value = (mock_stdout, mock_stderr)
        mock_create_subprocess.return_value = mock_process

        repo = RequestRepository()
        result = await repo.get_speedtest_results()

        mock_create_subprocess.assert_called_once_with(
            "/usr/bin/speedtest-cli",
            "--json",
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        assert result == mock_speedtest_output

    @pytest.mark.anyio
    @patch("src.repositories.requester.asyncio.create_subprocess_exec")
    @patch("src.repositories.requester.asyncio.wait_for")
    async def test_speedtest_timeout_exception(
        self, mock_wait_for, mock_create_subprocess
    ):
        """Test speedtest timeout handling"""
        mock_process = Mock()
        mock_create_subprocess.return_value = mock_process
        mock_wait_for.side_effect = asyncio.TimeoutError()

        repo = RequestRepository()

        with pytest.raises(Exception, match="Speedtest timed out"):
            await repo.get_speedtest_results()

    @pytest.mark.anyio
    @patch("src.repositories.requester.asyncio.create_subprocess_exec")
    @patch("src.repositories.requester.asyncio.wait_for")
    async def test_speedtest_process_error(self, mock_wait_for, mock_create_subprocess):
        """Test speedtest process error handling"""
        mock_process = Mock()
        mock_create_subprocess.return_value = mock_process
        mock_wait_for.side_effect = subprocess.CalledProcessError(1, "speedtest-cli")

        repo = RequestRepository()

        with pytest.raises(Exception, match="Speedtest failed with exit code 1"):
            await repo.get_speedtest_results()

    @pytest.mark.anyio
    @patch("src.repositories.requester.asyncio.create_subprocess_exec")
    @patch("src.repositories.requester.asyncio.wait_for")
    async def test_speedtest_json_parse_error(
        self, mock_wait_for, mock_create_subprocess
    ):
        """Test handling of invalid JSON response"""
        mock_process = Mock()
        mock_create_subprocess.return_value = mock_process
        mock_stdout = b"invalid json"
        mock_stderr = b""
        mock_wait_for.return_value = (mock_stdout, mock_stderr)

        repo = RequestRepository()

        with pytest.raises(Exception, match="Failed to parse speedtest JSON output"):
            await repo.get_speedtest_results()

    @pytest.mark.anyio
    @patch("src.repositories.requester.asyncio.create_subprocess_exec")
    @patch("src.repositories.requester.asyncio.wait_for")
    async def test_speedtest_generic_exception(
        self, mock_wait_for, mock_create_subprocess
    ):
        """Test handling of generic exceptions"""
        mock_process = Mock()
        mock_create_subprocess.return_value = mock_process
        mock_wait_for.side_effect = RuntimeError("Something went wrong")

        repo = RequestRepository()

        with pytest.raises(Exception, match="An error occurred"):
            await repo.get_speedtest_results()

    @pytest.mark.anyio
    @patch("src.repositories.requester.asyncio.create_subprocess_exec")
    @patch("src.repositories.requester.asyncio.wait_for")
    async def test_custom_timeout_used(
        self, mock_wait_for, mock_create_subprocess, mock_speedtest_output
    ):
        """Test that custom timeout is passed to wait_for"""
        mock_process = Mock()
        mock_stdout = json.dumps(mock_speedtest_output).encode()
        mock_stderr = b""
        mock_wait_for.return_value = (mock_stdout, mock_stderr)
        mock_create_subprocess.return_value = mock_process

        repo = RequestRepository(timeout=30)
        await repo.get_speedtest_results()

        # Check that wait_for was called with the custom timeout
        mock_wait_for.assert_called_once()
        call_args = mock_wait_for.call_args
        assert call_args[1]["timeout"] == 30
