from fastapi import HTTPException
from app.async_content_generation import generate_material
from app.config import MODEL
from app.models import CurriculumRequest, MarkdownCurriculumRequest
from app.utils import get_prompt, md_to_json
from fastapi import APIRouter
import app.system_prompts as sp
from . import client

router = APIRouter()


@router.post("/create_curriculum/")
async def create_curriculum(request: CurriculumRequest):
    try:
        ptext = sp.CURRICULUM_PROMPT
        prompt_text = get_prompt("generate_syllabus", dict(request), ptext)

        response = client.chat.completions.create(
            model=MODEL, messages=prompt_text, temperature=0.1
        )

        curriculum_text = response.choices[0].message.content
        return {"curriculum": curriculum_text}
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred while generating the curriculum: {str(e)}",
        )


@router.post("/generate_md/")
async def generate_md(request: MarkdownCurriculumRequest):
    try:
        curr = md_to_json(request.markdown_text)
        print(curr)

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred while converting to JSON: {str(e)}",
        )

    generate_material(curr, constraint=request.constraints, subject=request.subject)
    return {"message": "Material generated successfully"}
