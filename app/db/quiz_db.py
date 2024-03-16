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
    course_ref = db.collection(course_collection).document()  

    course_ref.set({
        "name": name,
        "course_code": course_code,
        "image_url": image_url,
    })

    course_id = course_ref.id  

    course_ref.update({
        "course_id": course_id  
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


def add_quiz(name,course_id, questions,end_date):
    quiz_ref = db.collection(quiz_collection).document()
    
    quiz_ref.set({
        "name":name,
        "course_id":course_id,
        "questions": questions,
        "end_date": end_date
    })
    quiz_id = quiz_ref.id
    
    quiz_ref.update({
        "quiz_id":quiz_id
    })
    return quiz_id


def submit_quiz(name,user_id, saved_answers, marks_scored):
    db.collection(submit_quiz_collection).add(
        {
            "name":name,
            "user_id": user_id,
            "saved_answers": saved_answers,
            "marks_scored": marks_scored,
        }
    )

def retreive_correct_answers(quiz_id):
    quiz_doc = db.collection(quiz_collection).document(quiz_id).get().to_dict()
    print('printing')
    data = quiz_doc['questions']
    correct_answer_values = [item['correct_answer'] for item in data]
    print(correct_answer_values)
    return correct_answer_values

def update_user_submitted_quiz(user_id: str, quiz_id: str):
    user_ref = db.collection(user_collection).document(user_id)  

    user_data = user_ref.get().to_dict()  
    submitted_quizzes = user_data.get('submitted_quizzes', [])  

    if quiz_id not in submitted_quizzes:
        submitted_quizzes.append(quiz_id)  

    user_ref.update({'submitted_quizzes': submitted_quizzes})  
    
def retreive_upcoming_quizes(student_id):
    user_ref = db.collection(user_collection).document(student_id)
    quizes=[]
    user_data = user_ref.get().to_dict()
    quiz_ref = db.collection(quiz_collection)
    query=quiz_ref.stream()
    
    course_list = user_data['course_list']
    quiz_ref = db.collection('quiz')
    query = quiz_ref.stream()
    
    for quiz in query:
        quiz_data = quiz.to_dict()
        for i in course_list:
            if quiz_data.get('course_id') == i:
                quizes.append(quiz_data)
    return quizes
        

def update_quiz(questions,quiz_id):
    quiz_ref = db.collection(quiz_collection).document(quiz_id)
    
    quiz_ref.update({'questions':questions})