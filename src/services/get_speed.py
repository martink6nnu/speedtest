from src.repositories.requester import RequestRepository
from src.models.speedresponse import SpeedResponse


class SpeedService:
    def __init__(self, request_repository: RequestRepository):
        self.request_repository = request_repository

    async def get_speedtest_results(self) -> SpeedResponse:
        results = await self.request_repository.get_speedtest_results()
        
        # Convert from bits per second to megabits per second (Mbps)
        download_mbps = round(results["download"] / 1_000_000, 2)
        upload_mbps = round(results["upload"] / 1_000_000, 2)
        
        return SpeedResponse(
            download_speed=download_mbps,
            upload_speed=upload_mbps,
            ping=results["ping"],
            server_name=results["server"]["name"],
            server_location=results["server"]["country"],
        )
