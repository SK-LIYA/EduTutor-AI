import streamlit as st

def is_logged_in():
    return st.session_state.get("logged_in", False)

def login_user(email):
    st.session_state["logged_in"] = True
    st.session_state["user_email"] = email

def logout_user():
    st.session_state["logged_in"] = False
    st.session_state["user_email"] = None
