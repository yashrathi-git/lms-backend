from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import logging
from rich.logging import RichHandler
from app.routes import generate_routes, quiz, update_quiz

logging.basicConfig(
    level="INFO", format="%(message)s", datefmt="[%X]", handlers=[RichHandler()]
)


origins = [
    "http://127.0.0.1:5500",
]


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(generate_routes.router)
app.include_router(quiz.router)
app.include_router(update_quiz.router)
