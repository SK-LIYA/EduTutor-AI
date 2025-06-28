from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import sqlite3
import hashlib

user_auth_router = APIRouter(
    prefix="/user",
    tags=["User"]
)

# Pydantic model
class User(BaseModel):
    email: str
    password: str

# Hashing utility
def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

# DB Initialization
def init_manual_user_db():
    conn = sqlite3.connect("students.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (
        email TEXT PRIMARY KEY,
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

    c.execute("INSERT INTO users (email, password) VALUES (?, ?)",
              (user.email, hash_password(user.password)))
    conn.commit()
    conn.close()
    return {"message": "✅ Registration successful!"}

# Login route
@user_auth_router.post("/login")
def login(user: User):
    conn = sqlite3.connect("students.db")
    c = conn.cursor()
    c.execute("SELECT password FROM users WHERE email=?", (user.email,))
    result = c.fetchone()
    conn.close()

    if result and result[0] == hash_password(user.password):
        return {"message": "✅ Login successful!"}
    raise HTTPException(status_code=401, detail="Invalid email or password")
