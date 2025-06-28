from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import sqlite3
import hashlib

user_auth_router = APIRouter(
    prefix="/user",
    tags=["User"]
)

# Pydantic model for registration
class User(BaseModel):
    username: str
    email: str
    password: str

# Pydantic model for login
class LoginUser(BaseModel):
    email: str
    password: str

# Password hashing utility
def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

# Initialize database with username field
def init_manual_user_db():
    conn = sqlite3.connect("students.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (
        email TEXT PRIMARY KEY,
        username TEXT,
        password TEXT
    )''')
    conn.commit()
    conn.close()

init_manual_user_db()

# Register route
@user_auth_router.post("/register")
def register(user: User):
    conn = sqlite3.connect("students.db")
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE email=?", (user.email,))
    if c.fetchone():
        conn.close()
        raise HTTPException(status_code=400, detail="User already exists")

    c.execute("INSERT INTO users (email, username, password) VALUES (?, ?, ?)",
              (user.email, user.username, hash_password(user.password)))
    conn.commit()
    conn.close()
    return {"message": f"✅ User {user.username} registered successfully!"}

# Login route
@user_auth_router.post("/login")
def login(user: LoginUser):
    conn = sqlite3.connect("students.db")
    c = conn.cursor()
    c.execute("SELECT username, password FROM users WHERE email=?", (user.email,))
    result = c.fetchone()
    conn.close()

    if result and result[1] == hash_password(user.password):
        return {"message": f"✅ Welcome back, {result[0]}!"}
    raise HTTPException(status_code=401, detail="Invalid email or password")
