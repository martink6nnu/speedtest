from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from src.dependencies import get_speed_service
from src.services.get_speed import SpeedService

router = APIRouter()


@router.get("/speed")
async def get_speed(speed_service: Annotated[SpeedService, Depends(get_speed_service)]):
    try:
        return await speed_service.get_speedtest_results()
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to get speed test results: {str(e)}"
        ) from e
