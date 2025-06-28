# routes/submission.py

from fastapi import APIRouter
from pydantic import BaseModel

submission_router = APIRouter(
    prefix="/quiz",
    tags=["Quiz Submission"]
)

class QuizSubmission(BaseModel):
    user_id: str
    quiz_id: str
    answers: dict  # or List[str] if answers are ordered

@submission_router.post("/submit")
def submit_quiz(submission: QuizSubmission):
    # Placeholder logic to store submission
    return {
        "message": f"Quiz {submission.quiz_id} submitted by user {submission.user_id}",
        "answers": submission.answers
    }
