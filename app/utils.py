import os
from fastapi import HTTPException
from rich.console import Console
from rich.text import Text
from rich.pretty import pprint

console = Console()


def _get_prompt(filename, variables):
    path = "app/prompts/"
    try:
        with open(os.path.join(path, filename), "r") as file:
            content = file.read()
    except FileNotFoundError:
        error_message = f"File {filename} not found in the prompts folder"
        console.print(Text(error_message, style="bold red"))
        raise HTTPException(status_code=404, detail=error_message)
    except Exception as e:
        error_message = f"An error occurred while reading the file: {str(e)}"
        console.print(Text(error_message, style="bold red"))
        raise HTTPException(status_code=500, detail=error_message)

    for key, value in variables.items():
        content = content.replace("{{" + str(key) + "}}", str(value))

    return content


def get_prompt(filename, variables, prompt_text):
    final_content = _get_prompt(filename=filename, variables=variables)

    structured_prompt = [
        {
            "role": "user",
            "content": final_content,
        },
        {
            "role": "system",
            "content": prompt_text,
        },
    ]

    console.print("[bold]Filename:[/bold]", filename)
    console.print("[bold]Variables:[/bold]", variables)

    pprint(structured_prompt)

    return structured_prompt
