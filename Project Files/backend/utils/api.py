import requests

BASE_URL = "http://127.0.0.1:8000"

def login_user_api(email, password):
    return requests.post(f"{BASE_URL}/login", json={"email": email, "password": password})

def register_user_api(email, password):
    return requests.post(f"{BASE_URL}/register", json={"email": email, "password": password})

def generate_quiz_api(topic):
    return requests.post(f"{BASE_URL}/generate-quiz", json={"topic": topic})
