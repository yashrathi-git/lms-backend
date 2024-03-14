import json
import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from openai import OpenAI
from dotenv import load_dotenv
from app.models import CurriculumRequest, MarkdownCurriculumRequest
import os

origins = [
    "http://127.0.0.1:5500",
]


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


def generate_material(subtopics: list, constraint: str, subject: str):
    try:
        generated_material = ""

        for i, subtopic in enumerate(subtopics):
            print("Subtopic: ", subtopic)
            generated_material += f"## {subtopic}\n\n"
            prompt_text = (
                f"I am learning {subject}. I am currently studying the topic: '{subtopics[0]}'. "
                f"Please write study material for the subtopic: '{subtopic}' in {subject}. "
                "You should start with a '##' heading for the subtopic title. "
                "For any subdivisions or additional headings within this subtopic, "
                "use '###' headings or lower. Do not use '##' headings except for the initial title of each subtopic."
                "Make sure to strictly follow the following constraint. They must be strictly adhered to:"
                f"{constraint}"
                "Keep the content concise."
            )
            messages = [
                {"role": "user", "content": prompt_text},
                {
                    "role": "system",
                    "content": "You're tasked to generate educational content. Keep it concise and informative.",
                },
            ]

            response = client.chat.completions.create(
                model="gpt-4",
                messages=messages,
                temperature=0.5,
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
        prompt_text = (
            "Convert the following markdown-formatted curriculum into a structured JSON format:\n\n"
            + request.markdown_text
            + "\nIf the input is - Topic:\n  - Subtopic 1\n  - Subtopic 2\n  - Subtopic 3\n\n"
            + '\n\nThe desired JSON structure is: [{"topic": "topicName", "subtopics": ["subtopic 1", "subtopic 2", "subtopic 3", "Sub Subtopic 1"]}, {"topic": "topicName", "subtopics": ["subtopic 1", "subtopic 2", "subtopic 3"]}]'
            + "\nThe subtopics list should be flat not nested."
            + "\nOnly give the JSON structure and noting else. It should be directely parsable."
        )

        messages = [
            {"role": "user", "content": prompt_text},
            {
                "role": "system",
                "content": "You are a teacher. Read the user demands carefully and generate the output.",
            },
        ]

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
    with open("out.md", "r") as f:
        return {"markdown": f.read()}
