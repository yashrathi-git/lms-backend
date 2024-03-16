from fastapi import APIRouter, HTTPException

from app.models import QuizRequest,SubmitQuizRequest
from app.utils import get_prompt
from app.config import MODEL
from app.routes import client
import app.system_prompts as sp
from app.db.quiz_db import add_quiz,submit_quiz, retreive_correct_answers, update_user_submitted_quiz, retreive_upcoming_quizes
import json
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
        print(quiz_text)
        add_quiz(request.course_id, json.loads(quiz_text),request.end_date)
        return quiz_text
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred while generating the quiz: {str(e)}",
        )
def calculate_marks(correct_answers,saved_answers):
    marks=0
    for i in range(len(correct_answers)):
        if(correct_answers[i] == saved_answers[i]):
            print("correct answer is "+correct_answers[i])
            print("saved is "+saved_answers[i])
            marks+=1
        return marks
@router.post("/save_student_answers/")
async def save_student_answers(request: SubmitQuizRequest):
    try:
        print(request.quiz_id)
        print(request.saved_answers)
        correct_answers = retreive_correct_answers(request.quiz_id)
        marks = calculate_marks(correct_answers,request.saved_answers,marks)
        submit_quiz(request.name,request.quiz_id,request.saved_answers,marks)
        update_user_submitted_quiz(request.student_id,request.quiz_id)
        print(request.saved_answers)
        print(request.quiz_id)
        print(request)
        return {"message": "Student answers saved successf0.0.ully for quiz ID: {quiz_id}"}

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred while saving student answers: {str(e)}"
        )

@router.post("/show_upcoming_quiz")
async def show_quiz():
    current_quizes = retreive_upcoming_quizes()
    return {"quizes": current_quizes}
    
    