from fastapi import APIRouter
from . import client

router = APIRouter()


@router.get("/get_explanation")
async def get_explanation(prompt: str):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": f"Explain the concept of {prompt}",
            }
        ],
        temperature=0.1,
    )
    explanation = response.choices[0].message.content
    return {"explanation": explanation}
