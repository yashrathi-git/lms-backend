import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import uuid
from . import db


user_collection = "users"
course_collection = "courses"
assignment_collection = "assignments"
quiz_collection = "quiz"
submit_quiz_collection = "submit_quiz"


def add_user(name, email, user_type):
    user_id = str(uuid.uuid4())

    db.collection(user_collection).document("2").set(
        {"user_id": user_id, "name": name, "email": email, "type": user_type}
    )

    print("User added successfully with ID:", user_id)


def add_course(name, course_code, image_url):
    course_id = str(uuid.uuid4())

    db.collection(course_collection).document(course_id).set(
        {
            "course_id": course_id,
            "name": name,
            "course_code": course_code,
            "image_url": image_url,
        }
    )

    print("Course added successfully with ID:", course_id)


def assign_course_to_user(user_id, course_id):
    user_ref = db.collection(user_collection).document(user_id)
    user_ref.update({"courseId": firestore.ArrayUnion([course_id])})

    print("Course assigned successfully to user with ID:", user_id)


def add_assignment(course_id, pdf_url, question, deadline):
    db.collection(assignment_collection).add(
        {
            "course_id": course_id,
            "pdf_url": pdf_url,
            "question": question,
            "deadline": deadline,
        }
    )


def add_quiz(course_id, questions):
    db.collection(quiz_collection).add({"course_id": course_id, "questions": questions})


def submit_quiz(user_id, saved_answers, marks_scored):
    db.collection(submit_quiz_collection).add(
        {
            "user_id": user_id,
            "saved_answers": saved_answers,
            "marks_scored": marks_scored,
        }
    )


# add_user("Modi","modi@gmail","teacher")
add_course(
    "dbms",
    "BCSE",
    "https://www.python.org/static/community_logos/python-logo-master-v3-TM.png",
)
# assign_course_to_user( "8184e5fb-d03d-4130-8d01-9e87dbc151df","39e8716f-ad5b-49a7-b492-3fcbece6d3b5")

questions = [
    {
        "question": "What is the capital of France?",
        "choices": ["Paris", "London", "Berlin", "Madrid"],
        "correct_answer": "Paris",
    },
    {
        "question": "Who invented the telephone?",
        "choices": [
            "Thomas Edison",
            "Alexander Graham Bell",
            "Albert Einstein",
            "Nikola Tesla",
        ],
        "correct_answer": "Alexander Graham Bell",
    },
]

# submit_quiz("8184e5fb-d03d-4130-8d01-9e87dbc151df",["Paris","Alexander Graham Bell"],10)

# add_assignment("39e8716f-ad5b-49a7-b492-3fcbece6d3b5","random_url","How to center a div in CSS?", "2021-12-31")
