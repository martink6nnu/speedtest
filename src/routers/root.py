from fastapi import APIRouter

router = APIRouter()


@router.get("/")
def read_root():
    return "hiiii :3"
