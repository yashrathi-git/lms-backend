import firebase_admin
from firebase_admin import credentials, firestore

cred = credentials.Certificate(
    "./smart-lms-aad55-firebase-adminsdk-9jorz-d1598512f8.json"
)
firebase_admin.initialize_app(cred)

db = firestore.client()
