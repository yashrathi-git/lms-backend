from fastapi import APIRouter, HTTPException

from app.db.notes_db import create_notes
from app.models import UpdateNotes

router = APIRouter()


@router.post("/update_notes")
async def update_notes(request: UpdateNotes):
    try:
        create_notes(
            request.user_id,
            request.subject,
            request.topic,
            request.subtopic,
            request.notes,
        )
        return {"message": "Notes updated successfully"}
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred while updating the notes: {str(e)}",
        )
