from fastapi import APIRouter

educator_router = APIRouter(
    prefix="/educator",
    tags=["Educator"]
)

@educator_router.get("/student/{user_id}/quiz-history")
def get_student_quiz_history(user_id: str):
    # Placeholder logic
    return {"user_id": user_id, "quiz_history": ["quiz1", "quiz2", "quiz3"]}
