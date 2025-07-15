from src.repositories.requester import RequestRepository
from src.models.speedresponse import SpeedResponse


class SpeedService:
    def __init__(self, request_repository: RequestRepository):
        self.request_repository = request_repository

    def get_speedtest_results(self) -> SpeedResponse:
        results = self.request_repository.get_speedtest_results()
        return SpeedResponse(
            download_speed=results["download"]["bandwidth"],
            upload_speed=results["upload"]["bandwidth"],
            ping=results["ping"],
            server_name=results["server"]["name"],
            server_location=results["server"]["location"],
        )
