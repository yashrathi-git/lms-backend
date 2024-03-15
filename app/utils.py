import os
from fastapi import HTTPException
import logging
from rich.logging import RichHandler

FORMAT = "%(asctime)s - [%(levelname)s] - %(message)s"
logging.basicConfig(
    level=logging.DEBUG,
    format=FORMAT,
    datefmt="[%X]",
    handlers=[RichHandler(rich_tracebacks=True)],
)

log = logging.getLogger("rich")


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
        {
            "role": "system",
            "content": prompt_text,
        },
        {
            "role": "user",
            "content": _get_prompt(filename=filename, variables=variables),
        },
    ]
    log.info("Filename: %s", filename)
    log.info("Variables: %s", variables)
    log.info("Prompt Text: %s", prompt_text)
    log.info(prompt_text)
    return _get_prompt(filename, variables)
