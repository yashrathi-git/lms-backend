from app.async_content_generation import generate_material
from app.utils import md_to_json

curriculum = """
- Introduction to Machine Learning
    - What is Machine Learning?
    - Types of Machine Learning
    - Applications of Machine Learning

- Basic Concepts of Machine Learning
    - Understanding Data and Datasets
    - Features and Labels in Data
    - Training and Testing Data

- Simple Machine Learning Algorithms
    - Linear Regression
    - Decision Trees
    - K-Nearest Neighbors


""".strip()
generate_material(
    curr=md_to_json(curriculum),
    constraint="Teach me like I am 5 year old. Make it short, not more than 3 topics, just give an overview",
    subject="Machine Learning",
    user_id="cache",
)
