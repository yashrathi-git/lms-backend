from fastapi import APIRouter, HTTPException

from app.models import QuizRequest
from app.utils import get_prompt
from app.config import MODEL
from app.routes import client
import app.system_prompts as sp


router = APIRouter()


@router.post("/generate_quiz/")
async def generate_quiz(request: QuizRequest):
    try:
        ptext = sp.GENERATE_QUIZ_PROMPT
        prompt_text = get_prompt("generate_quiz", dict(request), ptext)

        response = client.chat.completions.create(
            model=MODEL, messages=prompt_text, temperature=0.1
        )

        quiz_text = response.choices[0].message.content
        cleaned_data = quiz_text.replace("\\", "").replace("\\n", "")
        return cleaned_data

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred while generating the quiz: {str(e)}",
        )
