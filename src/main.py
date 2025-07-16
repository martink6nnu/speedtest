from fastapi import FastAPI

from src.routers import root, speed

app = FastAPI()
app.include_router(root.router)
app.include_router(speed.router)
