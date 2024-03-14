from pydantic import BaseModel


class CurriculumRequest(BaseModel):
    syllabus: str
    constraints: str
    subject: str


class MarkdownCurriculumRequest(BaseModel):
    markdown_text: str
    constraints: str
    subject: str
