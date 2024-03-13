from pydantic import BaseModel


class CurriculumRequest(BaseModel):
    syllabus: str
    constraints: str
    subject: str
