from fastapi import APIRouter

from app.models import SubjectiveGenerate
from . import client
from app.db import db

router = APIRouter()


@router.get("/get_explanation")
async def get_explanation(prompt: str):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": f"Explain the concept of {prompt}",
            }
        ],
        temperature=0.1,
    )
    explanation = response.choices[0].message.content
    return {"explanation": explanation}


@router.post("/generate_subjective")
async def generate_subjective(request: SubjectiveGenerate):
    doc_ref = db.collection("subjective_quiz").document()
    doc_ref.set(dict(request))

    return {"message": "Data stored successfully"}


@router.post("/submit_subjective")
async def submit_subjective(request: SubjectiveGenerate):
    quiz = db.collection("subjective_quiz").where("name", "==", request.name)
    # Quiz would only be one quiz
    quiz = quiz.stream()
    quiz = list(quiz)
    quiz = quiz[0].to_dict()
