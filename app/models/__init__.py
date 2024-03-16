from pydantic import BaseModel

import datetime
import typing as t


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
    course_id: str
    end_date: datetime.datetime


class SubmitQuizRequest(BaseModel):
    saved_answers: list
    quiz_id: str
    student_id: str
    name: str


class SubjectiveGenerate(BaseModel):
    name: str
    subject: str
    questions: t.List[str]
    constraints: t.List[str]
    marks: t.List[int]
    course_id: str
    end_date: datetime.datetime


class SubjectiveSubmit(BaseModel):
    user_id: str
    saved_answers: t.List[str]
    quiz_id: str
    name: str
    course_id: str
    end_date: datetime.datetime
