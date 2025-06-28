from fastapi import APIRouter, HTTPException  # Removed `Header`
from pydantic import BaseModel
from dotenv import load_dotenv
# from google.oauth2.credentials import Credentials  #  Commented out Google Classroom auth
# from googleapiclient.discovery import build       #  Commented out Google Classroom API
import os
import requests
import json
import re

# Load environment variables
load_dotenv()

quiz_router = APIRouter(
    prefix="/quiz",
    tags=["Quiz"]
)

class QuizRequest(BaseModel):
    topic: str
    num_questions: int

def get_ibm_token():
    url = "https://iam.cloud.ibm.com/identity/token"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    data = {
        "apikey": os.getenv("WATSONX_API_KEY"),
        "grant_type": "urn:ibm:params:oauth:grant-type:apikey"
    }
    response = requests.post(url, headers=headers, data=data)
    if response.status_code == 200:
        return response.json()["access_token"]
    else:
        raise Exception(f"Failed to get IBM token: {response.text}")

@quiz_router.post("/generate")
def generate_quiz(payload: QuizRequest):
    
    # if not authorization:
    #     raise HTTPException(status_code=401, detail="Authorization token missing.")
    #
    # access_token = authorization.split(" ")[1]
    #
    # credentials = Credentials(
    #     token=access_token,
    #     token_uri='https://oauth2.googleapis.com/token',
    #     client_id=os.getenv("GOOGLE_CLIENT_ID"),
    #     client_secret=os.getenv("GOOGLE_CLIENT_SECRET"),
    #     scopes=["https://www.googleapis.com/auth/classroom.courses.readonly"]
    # )
    #
    # service = build("classroom", "v1", credentials=credentials)
    #
    # course_materials = ""
    # try:
    #     courses = service.courses().list().execute().get("courses", [])
    #     for course in courses:
    #         try:
    #             coursework = service.courses().courseWork().list(courseId=course["id"]).execute()
    #             for item in coursework.get("courseWork", []):
    #                 if payload.topic.lower() in item.get("title", "").lower():
    #                     course_materials += item.get("description", "") + "\n"
    #         except Exception as e:
    #             print(f"⚠️ Error reading coursework: {e}")
    # except Exception as e:
    #     raise HTTPException(status_code=500, detail=f"Error fetching Google Classroom courses: {str(e)}")
    #
    # if not course_materials:
    #     raise HTTPException(status_code=404, detail="No relevant content found in Google Classroom.")

    # ✅ Replaced with simple course material if no auth/token
    course_materials = f"This is some basic content on the topic: {payload.topic}."

    # ✅ WatsonX prompt
    prompt = (
        f"Use the following content to generate a quiz:\n\n"
        f"{course_materials}\n\n"
        f"Generate {payload.num_questions} multiple choice questions (MCQs). "
        f"For each question, include:\n"
        f"- 'question': the text of the question\n"
        f"- 'options': a list of 4 answer choices\n"
        f"- 'answer': the correct answer\n"
        f"Return ONLY a valid JSON array of question objects. No explanation. No markdown. No code block.\n"
        f"Do not wrap it in a Python tuple or return extra text. Do not truncate the last question."
    )

    ibm_token = get_ibm_token()
    url = f"{os.getenv('WATSONX_ENDPOINT')}/ml/v1/text/generation?version=2023-05-29"
    headers = {
        "Authorization": f"Bearer {ibm_token}",
        "Content-Type": "application/json"
    }
    payload_data = {
        "model_id": os.getenv("WATSONX_MODEL_ID"),
        "input": prompt,
        "parameters": {
            "decoding_method": "greedy",
            "max_new_tokens": 1500
        },
        "project_id": os.getenv("WATSONX_PROJECT_ID")
    }

    response = requests.post(url, headers=headers, json=payload_data)
    if response.status_code == 200:
        try:
            raw_output = response.json()["results"][0]["generated_text"]
            if isinstance(raw_output, (tuple, list)):
                raw_text = raw_output[0]
            else:
                raw_text = raw_output
            print("🔍 WatsonX output:\n", raw_text)
            # Use regex to extract just the JSON array part (non-greedy)
            match = re.search(r"\[\s*{.*?}\s*\]", raw_text, re.DOTALL)
            if not match:
                raise ValueError("No valid JSON array found in WatsonX output.")
            cleaned_json_str = match.group(0)
            while True:
                try:
                    questions = json.loads(cleaned_json_str)
                    break
                except json.JSONDecodeError:
                    cleaned_json_str = cleaned_json_str.strip()[:-1]  # Trim 1 char
                    if len(cleaned_json_str) < 10:
                        raise HTTPException(status_code=500, detail="Output too corrupted to parse.")

            return {"questions": questions}

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to parse WatsonX output: {str(e)}")

    