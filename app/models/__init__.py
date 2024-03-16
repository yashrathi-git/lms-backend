from pydantic import BaseModel

import datetime

class CurriculumRequest(BaseModel):
    syllabus: str
    constraints: str
    subject: str


class MarkdownCurriculumRequest(BaseModel):
    markdown_text: str
    constraints: str
    subject: str
    user_id: str


class UpdateNotes(BaseModel):
    notes: str
    user_id: str
    subject: str
    topic: str
    subtopic: str
    note_id: str


class QuizRequest(BaseModel):
    subject: str
    constraints: str
    number: str
    course_id:str
    end_date: datetime.datetime
    

class SubmitQuizRequest(BaseModel):
    saved_answers : list
    quiz_id:str
    student_id:str
    name:str