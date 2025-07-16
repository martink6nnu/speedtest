from typing import Annotated

from fastapi import Depends

from src.repositories.requester import RequestRepository
from src.services.get_speed import SpeedService


def get_request_repository() -> RequestRepository:
    return RequestRepository()


def get_speed_service(
    request_repository: Annotated[RequestRepository, Depends(get_request_repository)],
) -> SpeedService:
    return SpeedService(request_repository)
