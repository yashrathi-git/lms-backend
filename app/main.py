import json
import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from .utils import md_to_json
from openai import OpenAI
from dotenv import load_dotenv
from app.models import CurriculumRequest, MarkdownCurriculumRequest
import app.system_prompts as sp
from app.utils import get_prompt
import os
import logging
from rich.logging import RichHandler
from .async_content_generation import generate_material
from .config import MODEL, OPENAI_API_KEY
from .db import create_wireframe
from rich.traceback import install

install()


logging.basicConfig(
    level="INFO", format="%(message)s", datefmt="[%X]", handlers=[RichHandler()]
)


origins = [
    "http://127.0.0.1:5500",
]


client = OpenAI(api_key=OPENAI_API_KEY)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/create_curriculum/")
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


@app.post("/generate_md/")
async def generate_md(request: MarkdownCurriculumRequest):
    try:
        curr = md_to_json(request.markdown_text)
        print(curr)

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred while converting to JSON: {str(e)}",
        )

    create_wireframe("default_userid2", request.subject, curr)
    generate_material(curr, constraint=request.constraints, subject=request.subject)
    with open("out.md", "r") as f:
        return {"markdown": f.read()}
