from fastapi import APIRouter, Depends, HTTPException
from src.services.get_speed import SpeedService
from src.dependencies import get_speed_service

router = APIRouter()

@router.get("/speed")
def get_speed(speed_service: SpeedService = Depends(get_speed_service)):
    try:
        return speed_service.get_speedtest_results()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get speed test results: {str(e)}")

