from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from dotenv import load_dotenv
import os
import threading
import webbrowser

# ✅ Load environment variables from .env
load_dotenv()

# ✅ Initialize FastAPI app
app = FastAPI(
    title="EduTutor AI",
    version="0.1.0"
)

# ✅ Middleware for OAuth sessions
app.add_middleware(SessionMiddleware, secret_key=os.getenv("SECRET_KEY", "default_secret"))

# ✅ CORS to allow frontend (Streamlit) to access FastAPI
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can restrict to Streamlit URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Root endpoint
@app.get("/")
def root():
    return {"message": "Welcome to EduTutor AI!"}

# ✅ Import and register routers
from routes.quiz import quiz_router
from routes.auth import auth_router
from routes.user_auth import user_auth_router
from routes.submission import submission_router
from routes.educator import educator_router

app.include_router(quiz_router)           # Quiz generation & retrieval
app.include_router(auth_router)           # Google OAuth login
app.include_router(user_auth_router)      # Register/Login with email/password
app.include_router(submission_router)     # Quiz submission, scoring
app.include_router(educator_router)       # Educator analytics dashboard

# ✅ Automatically open Swagger UI in browser when server starts
def open_docs():
    webbrowser.open_new("http://127.0.0.1:8000/docs")

threading.Timer(1.0, open_docs).start()
