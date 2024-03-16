from fastapi import HTTPException
from app.config import MODEL, OPENAI_API_KEY
from app.db.notes_db import create_notes
from app.utils import get_prompt
import app.system_prompts as sp
from openai import OpenAI

# Assuming OPENAI_API_KEY & MODEL are defined in your app.config
client = OpenAI(api_key=OPENAI_API_KEY)


def subtopic_generate_material(
    subtopics: list, constraint: str, subject: str, user_id: str, topic: str
):
    try:
        for subtopic in subtopics:
            print("Subtopic: ", subtopic)

            # Prepare the prompt text for each subtopic
            messages = get_prompt(
                "generate_material",
                {"subtopic": subtopic, "constraint": constraint},
                sp.GENERATE_MATERIAL_PROMPT,
            )

            response = client.chat.completions.create(
                model=MODEL,
                messages=messages,
                temperature=0.1,
            )

            content = response.choices[0].message.content
            create_notes(user_id, subject, topic, subtopic, content)

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred while generating material for subtopics: {str(e)}",
        )


def generate_material(curr, constraint, subject, user_id="default_userid"):
    print("Generating")

    try:
        for t in curr:
            topic = t["topic"]
            print("Gen Topic: ", topic)

            # Now integrates directly with Firebase instead of writing to a file
            subtopic_generate_material(
                t["subtopics"], constraint, subject, user_id, topic
            )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail="An error occurred while generating material: " + str(e),
        )
