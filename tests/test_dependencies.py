from src.dependencies import get_request_repository, get_speed_service
from src.repositories.requester import RequestRepository
from src.services.get_speed import SpeedService


class TestDependencies:
    """Test cases for dependency injection functions"""

    def test_get_request_repository(self):
        """Test that get_request_repository returns a RequestRepository instance"""
        repo = get_request_repository()
        
        assert isinstance(repo, RequestRepository)
        assert repo.timeout == 120  # Default timeout

    def test_get_request_repository_multiple_calls(self):
        """Test that multiple calls return new instances"""
        repo1 = get_request_repository()
        repo2 = get_request_repository()
        
        assert isinstance(repo1, RequestRepository)
        assert isinstance(repo2, RequestRepository)
        # Should be different instances (not singleton)
        assert repo1 is not repo2

    def test_get_speed_service(self, mock_request_repository):
        """Test that get_speed_service returns a SpeedService instance"""
        service = get_speed_service(mock_request_repository)
        
        assert isinstance(service, SpeedService)
        assert service.request_repository == mock_request_repository

    def test_get_speed_service_with_real_repository(self):
        """Test get_speed_service with real RequestRepository"""
        repo = get_request_repository()
        service = get_speed_service(repo)
        
        assert isinstance(service, SpeedService)
        assert isinstance(service.request_repository, RequestRepository)

    def test_dependency_chain(self):
        """Test the complete dependency chain"""
        # This simulates how FastAPI would resolve dependencies
        repo = get_request_repository()
        service = get_speed_service(repo)
        
        assert isinstance(repo, RequestRepository)
        assert isinstance(service, SpeedService)
        assert service.request_repository is repo

    def test_multiple_speed_service_instances(self):
        """Test that multiple speed service instances can be created"""
        repo1 = get_request_repository()
        repo2 = get_request_repository()
        
        service1 = get_speed_service(repo1)
        service2 = get_speed_service(repo2)
        
        assert service1 is not service2
        assert service1.request_repository is not service2.request_repository

    def test_speed_service_dependency_injection_interface(self):
        """Test that SpeedService correctly uses injected repository"""
        repo = get_request_repository()
        service = get_speed_service(repo)
        
        # Verify the service has the expected interface
        assert hasattr(service, 'get_speedtest_results')
        assert hasattr(service, 'request_repository')
        assert callable(service.get_speedtest_results) 