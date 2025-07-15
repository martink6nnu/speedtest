from pydantic import BaseModel


class SpeedResponse(BaseModel):
    download_speed: float
    upload_speed: float
    ping: float
    server_name: str
    server_location: str
