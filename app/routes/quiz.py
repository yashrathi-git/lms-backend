from fastapi import APIRouter, HTTPException

from app.models import QuizRequest,SubmitQuizRequest, UpdateQuiz, ShowUpcomingQuiz
from app.utils import get_prompt
from app.config import MODEL
from app.routes import client
import app.system_prompts as sp
from app.db.quiz_db import add_quiz,submit_quiz, retreive_correct_answers, update_user_submitted_quiz, retreive_upcoming_quizes, update_quiz
import json
router = APIRouter()

def add_quiz_id(quiz_text,quiz_id):
    for question in quiz_text:
        question['quiz_id']=quiz_id
    return quiz_text

@router.post("/generate_quiz/")
async def generate_quiz(request: QuizRequest):
    
    ptext = sp.GENERATE_QUIZ_PROMPT
    prompt_text = get_prompt("generate_quiz", dict(request), ptext)

    response = client.chat.completions.create(
        model=MODEL, messages=prompt_text, temperature=0.1
    )

    quiz_text = response.choices[0].message.content
    
    quiz_id=add_quiz(request.name,request.course_id, json.loads(quiz_text),request.end_date)
    quiz_text=json.loads(quiz_text)
    quiz_text=add_quiz_id(quiz_text,quiz_id)
    print(quiz_text)
    return quiz_text
    # except Exception as e:
    #     raise HTTPException(
    #         status_code=500,
    #         detail=f"An error occurred while generating the quiz: {str(e)}",
    #     )
def calculate_marks(correct_answers,saved_answers):
    marks=0
    for i in range(len(correct_answers)):
        if(correct_answers[i] == str(saved_answers[i])):
            marks+=1
        return marks
    
@router.post("/save_student_answers/")
async def save_student_answers(request: SubmitQuizRequest):
    try:
        print(request.quiz_id)
        print(request.saved_answers)
        correct_answers = retreive_correct_answers(request.quiz_id)
        marks = calculate_marks(correct_answers,request.saved_answers)
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
async def show_quiz(request:ShowUpcomingQuiz):
    current_quizes = retreive_upcoming_quizes(request.student_id)
    return {"quizes": current_quizes}
    

@router.post("/update_quiz")
async def update(request:UpdateQuiz):
    update_quiz(request.questions,request.quiz_id)