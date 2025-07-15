from fastapi import APIRouter, Depends
from src.services.get_speed import SpeedService
from src.dependencies import get_speed_service

router = APIRouter()

@router.get("/speed")
def get_speed(speed_service: SpeedService = Depends(get_speed_service)):
    return speed_service.get_speedtest_results()

