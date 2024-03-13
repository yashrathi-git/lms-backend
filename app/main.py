import os
from fastapi import FastAPI, HTTPException
from openai import OpenAI
from dotenv import load_dotenv
from app.models import CurriculumRequest
import os

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=OPENAI_API_KEY)

app = FastAPI()


def get_prompt(filename, variables):
    path = "app/prompts/"
    try:
        with open(os.path.join(path, filename), "r") as file:
            content = file.read()
    except FileNotFoundError:
        raise HTTPException(
            status_code=404, detail=f"File {filename} not found in the prompts folder"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred while reading the file: {str(e)}",
        )
    for key, value in variables.items():
        content = content.replace(f"{{{key}}}", str(value))

    return content


@app.post("/create_curriculum/")
async def create_curriculum(request: CurriculumRequest):
    try:
        prompt_text = [
            {"role": "user", "content": get_prompt("generate_syllabus", dict(request))},
            {
                "role": "system",
                "content": "You are a teacher. An AI assistant that will help in generating a cirriculum a teacher. Read the user demands carefully and generate the output.",
            },
        ]

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
