from fastapi import HTTPException

from app.config import MODEL, OPENAI_API_KEY
from app.utils import get_prompt
import app.system_prompts as sp

from openai import OpenAI, AsyncOpenAI


client = OpenAI(api_key=OPENAI_API_KEY)


def subtopic_generate_material(subtopics: list, constraint: str, subject: str):
    try:
        generated_material = ""

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
                model=MODEL,
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


def generate_material(curr, constraint, subject):
    print("Generating")
    c = ""
    try:
        for t in curr:
            topic = t["topic"]
            print("Gen Topic: ", topic)

            c += "# " + t["topic"] + "\n\n"
            c += subtopic_generate_material(t["subtopics"], constraint, subject)
        print(c)
        print("Writing to file")
        with open("out.md", "a") as f:
            f.write(c + "\n\n")
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred while generating material for subtopics: {str(e)}",
        )
