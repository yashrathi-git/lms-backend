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
    prompt: str
    number: str
    difficulty:str
    course_id:str
    end_date: str
    context:str
    name: str

class SubmitQuizRequest(BaseModel):
    saved_answers : list
    quiz_id:str
    student_id:str
    name:str


class SubjectiveQuestion(BaseModel):
    question: str
    constraints: t.List[str]
    marks: t.List[int]


class SubjectiveGenerate(BaseModel):
    name: str
    questions: t.List[SubjectiveQuestion]
    course_id: str
    end_date: datetime.datetime


class SubjectiveSubmit(BaseModel):
    user_id: str
    saved_answers: t.List[str]
    subject: str
    name: str
    course_id: str
    end_date: datetime.datetime
    
    
class UpdateQuiz(BaseModel):
    questions: list
    quiz_id : str
    
    
class ShowUpcomingQuiz(BaseModel):
    student_id:str
