import os
from fastapi import HTTPException


def _get_prompt(filename, variables):
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


def get_prompt(filename, variables, prompt_text):
    prompt_text = [
        {"role": "user", "content": get_prompt(filename=filename, variables=variables)},
        {
            "role": "system",
            "content": prompt_text,
        },
    ]
    return _get_prompt(filename, variables)
