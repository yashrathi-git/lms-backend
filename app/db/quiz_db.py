import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import uuid
from . import db
from datetime import datetime


user_collection = "users"
course_collection = "courses"
assignment_collection = "assignments"
quiz_collection = "quiz"
submit_quiz_collection = "submit_quiz"


def add_user(name, email, user_type,course_list):
    user_ref = db.collection(user_collection).document()
    
    user_ref.set({
        "name":name,
        "email":email,
        "user_type":user_type,
        "course_list":course_list,
        "submitted_quiz":[]
    })
    user_id= user_ref.id

    user_ref.update({
        "user_id":user_id
    })
    print("User added successfully with ID:", user_id)


def add_course(name, course_code, image_url):
    course_ref = db.collection(course_collection).document()  # Create a new document reference

    course_ref.set({
        "name": name,
        "course_code": course_code,
        "image_url": image_url,
    })

    course_id = course_ref.id  # Get the auto-generated course ID

    course_ref.update({
        "course_id": course_id  # Update the document with the actual course ID
    })

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


def add_quiz(course_id, questions,end_date):
    db.collection(quiz_collection).add({"course_id": course_id, "questions": questions, "end_date":end_date})


def submit_quiz(user_id, saved_answers, marks_scored):
    db.collection(submit_quiz_collection).add(
        {
            "user_id": user_id,
            "saved_answers": saved_answers,
            "marks_scored": marks_scored,
        }
    )

def retreive_correct_answers(quiz_id):
    quiz_doc = db.collection(quiz_collection).document(quiz_id).get().to_dict()
    #quiz_questions = quiz_doc['questions']
    print('printing')
    data = quiz_doc['questions']
    correct_answer_values = [item['correct_answer'] for item in data]
    print(correct_answer_values)
    return correct_answer_values

def update_user_submitted_quiz(user_id: str, quiz_id: str):
    user_ref = db.collection(user_collection).document(user_id)  # Assuming 'users' collection in Firestore

    user_data = user_ref.get().to_dict()  # Get the user's existing data
    submitted_quizzes = user_data.get('submitted_quizzes', [])  # Get the list of submitted quizzes or an empty list

    if quiz_id not in submitted_quizzes:
        submitted_quizzes.append(quiz_id)  # Append the new quiz ID if it's not already in the list

    user_ref.update({'submitted_quizzes': submitted_quizzes})  # Update the user's document with the modified list
    
def retreive_upcoming_quizes():
    current_datetime = datetime.now()
    active_quizzes = []
    quiz_ref = db.collection(quiz_collection)
    query = quiz_ref.where('end_date', '>', current_datetime).stream()
    print(query)
    for quiz in query:
        quiz_data = quiz.to_dict()
        active_quizzes.append(quiz_data)

    return active_quizzes

quiz = retreive_upcoming_quizes()
print('print')
print(quiz)