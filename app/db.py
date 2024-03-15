import firebase_admin
from firebase_admin import credentials, firestore

cred = credentials.Certificate(
    "./smart-lms-aad55-firebase-adminsdk-9jorz-d1598512f8.json"
)
firebase_admin.initialize_app(cred)


def create_notes(user_id, subject_name, topic_name, subtopic_name, notes_content):
    db = firestore.client()
    notes_doc_ref = db.collection("notes").document(user_id)

    doc = notes_doc_ref.get()
    if doc.exists:
        data = doc.to_dict()
        if subject_name not in data:
            data[subject_name] = []

        # Find the topic in the array
        topic_found = None
        for topic in data[subject_name]:
            if topic.get("name") == topic_name:
                topic_found = topic
                break

        if not topic_found:
            topic_found = {"name": topic_name, "subtopics": []}
            data[subject_name].append(topic_found)

        topic_found["subtopics"].append(
            {"name": subtopic_name, "content": notes_content}
        )

        notes_doc_ref.set(data)
    else:
        # Document does not exist, create new structure
        notes_doc_ref.set(
            {
                subject_name: [
                    {
                        "name": topic_name,
                        "subtopics": [
                            {"name": subtopic_name, "content": notes_content}
                        ],
                    }
                ]
            }
        )
