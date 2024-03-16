import firebase_admin
from firebase_admin import credentials, firestore
from . import db


def create_notes(user_id, subject_name, topic_name, subtopic_name, notes_content):
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


def update_notes(user_id, subject_name, topic_name, subtopic_name, new_content):
    db = firestore.client()
    notes_doc_ref = db.collection("notes").document(user_id)

    doc = notes_doc_ref.get()
    if not doc.exists:
        print("No such document!")
        return

    data = doc.to_dict()
    subject_data = data.get(subject_name)

    if subject_data is None:
        print(f"No such subject: {subject_name}")
        return

    # Find the topic
    for topic in subject_data:
        if topic.get("name") == topic_name:
            # Find the subtopic
            for subtopic in topic.get("subtopics", []):
                if subtopic.get("name") == subtopic_name:
                    # Update content
                    subtopic["content"] = new_content
                    break
            else:
                print(f"No such subtopic: {subtopic_name}")
                return
            break
    else:
        print(f"No such topic: {topic_name}")
        return

    # Update Firestore document
    notes_doc_ref.set(data)

    print(
        f"Successfully updated content for {subtopic_name} in {topic_name} under {subject_name}."
    )


if __name__ == "__main__":
    update_notes(
        "default_userid",
        "Javascript",
        "Brief History of JavaScript",
        "I am an experienced Python developer, I already knows the basics of the language, so it should be a fast-paced course.",
        "This is a tesdt updateingasdas?",
    )
