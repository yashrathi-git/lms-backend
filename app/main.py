import json
import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from openai import OpenAI
from dotenv import load_dotenv
from app.models import CurriculumRequest, MarkdownCurriculumRequest
import app.system_prompts as sp
from app.utils import get_prompt
import os

origins = [
    "http://127.0.0.1:5500",
]
MODEL = "gpt-4"

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


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
            model="gpt-4", messages=prompt_text, temperature=0.1
        )

        curriculum_text = response.choices[0].message.content
        return {"curriculum": curriculum_text}
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred while generating the curriculum: {str(e)}",
        )


def generate_material(subtopics: list, constraint: str, subject: str):
    try:
        generated_material = ""  # Initialize with a main Heading

        for i, subtopic in enumerate(subtopics):
            print("Subtopic: ", subtopic)
            generated_material += f"## {subtopic}\n\n"
            # Prepare the prompt text for each subtopic
            messages = get_prompt(
                "generate_material",
                {"subtopic": subtopic, "constraint": constraint},
                sp.GENERATE_MATERIAL_PROMPT,
            )

            response = client.chat.completions.create(
                model="gpt-4",
                messages=messages,
                temperature=0.1,
            )

            content = response.choices[0].message.content

            if i == 0:
                generated_material += content + "\n"
            else:
                adjusted_content = content.replace("## ", "### ", 1)
                generated_material += adjusted_content + "\n"

        return generated_material

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred while generating material for subtopics: {str(e)}",
        )


def gen(md_json, constraint, subject):
    print("Generating")
    c = ""
    try:
        curriculum_json = json.loads(md_json)
        for t in curriculum_json:
            topic = t["topic"]
            print("Gen Topic: ", topic)

            c += "# " + t["topic"] + "\n\n"
            c += generate_material(t["subtopics"], constraint, subject)
        print(c)
        print("Writing to file")
        with open("out.md", "a") as f:
            f.write(c + "\n\n")
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred while generating material for subtopics: {str(e)}",
        )


@app.post("/generate_md/")
async def generate_md(request: MarkdownCurriculumRequest):
    try:
        messages = get_prompt(
            "convert_to_json",
            {"markdown_text": request.markdown_text},
            sp.CONVERT_TO_JSON_PROMPT,
        )
        response = client.chat.completions.create(
            model="gpt-4", messages=messages, temperature=0.1, max_tokens=512
        )

        curriculum_json = response.choices[0].message.content

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred while converting to JSON: {str(e)}",
        )

    gen(curriculum_json, constraint=request.constraints, subject=request.subject)
    # return the out.md file
    with open("out.md", "r") as f:
        return {"markdown": f.read()}
