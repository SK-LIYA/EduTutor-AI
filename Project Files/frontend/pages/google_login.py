import streamlit as st

st.set_page_config(page_title="Google Classroom Login")

# Configure FastAPI backend URL
FASTAPI_BACKEND = "http://localhost:8000"

st.title("🔐 Login with Google to Access Google Classroom")

# Login button that redirects to FastAPI Google OAuth login
login_url = f"{FASTAPI_BACKEND}/auth/login"
st.markdown(f"[Click here to login with Google]({login_url})", unsafe_allow_html=True)

# Show login status from FastAPI session
st.info("After login, please go to: http://localhost:8501 to use the platform.")

st.stop()  # Prevent the rest from running if not logged in
