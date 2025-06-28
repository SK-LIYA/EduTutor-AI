import streamlit as st
import requests
from streamlit_option_menu import option_menu

st.set_page_config(page_title="EduTutor AI", layout="wide")
st.markdown("<style>" + open("style.css").read() + "</style>", unsafe_allow_html=True)

# Sidebar role selector
role = st.sidebar.selectbox("Login as:", ["Student", "Educator"])

# ----------------- STUDENT PANEL --------------------
if role == "Student":
    selected = option_menu(
        menu_title="EduTutor Student Panel",
        options=["Login", "Register", "Dashboard", "Quiz History"],
        icons=["box-arrow-in-right", "pencil", "graph-up", "book"],
        menu_icon="cast",
        default_index=0,
        orientation="horizontal",
    )

    # ---- LOGIN ----
    if selected == "Login":
        st.title("👩‍🎓 Student Login")
        email = st.text_input("Email", key="email_input")
        password = st.text_input("Password", type="password", key="password_input")

        if st.button("Login"):
            if email and password:
                response = requests.post(
                    "http://127.0.0.1:8000/user/login",
                    json={"email": email, "password": password}
                )
                if response.status_code == 200:
                    data = response.json()
                    st.success("✅ Login successful!")
                    st.session_state["logged_in"] = True
                    st.session_state["user_email"] = email
                    st.session_state["access_token"] = data.get("access_token")  # ✅ Save token for header auth
                    st.switch_page("pages/students_dashboard.py")
                else:
                    st.error("❌ Login failed. Check your credentials.")
            else:
                st.warning("Please enter both email and password.")

    # ---- REGISTER ----
    elif selected == "Register":
        st.title("📝 Student Registration")
        username = st.text_input("Username", key="reg_username")
        new_email = st.text_input("Email", key="reg_email")
        new_password = st.text_input("Password", type="password", key="reg_pass")

        if st.button("Register"):
            if username and new_email and new_password:
                response = requests.post(
                    "http://127.0.0.1:8000/user/register",
                    json={"username": username, "email": new_email, "password": new_password}
                )
                if response.status_code == 200:
                    st.success("✅ Registered successfully! Please log in.")
                else:
                    st.error("❌ Registration failed. Try a different email.")
            else:
                st.warning("Please fill all fields.")

    # ---- DASHBOARD ----
    elif selected == "Dashboard":
        if st.session_state.get("logged_in"):
            st.info(f"📊 Welcome to your dashboard, {st.session_state.get('user_email')}!")
        else:
            st.warning("🔒 Please log in first.")

    # ---- QUIZ HISTORY ----
    elif selected == "Quiz History":
        if st.session_state.get("logged_in"):
            st.warning("📚 Quiz history integration with Pinecone coming soon!")
        else:
            st.warning("🔒 Please log in first.")

# ----------------- EDUCATOR PANEL --------------------
elif role == "Educator":
    st.title("📈 Educator Dashboard")
    st.info("Coming soon: View student analytics and scores.")
