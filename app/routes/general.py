from fastapi import APIRouter


router = APIRouter()


@router.get("/get_upcoming")
async def get_upcoming():
    return {"message": "This is a test message"}
