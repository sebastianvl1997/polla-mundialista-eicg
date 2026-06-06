ADMIN_EMAIL = "sebastianvl1997@gmail.com"

def get_user():
    import streamlit as st
    return st.session_state.get("user")

def is_admin():
    user = get_user()
    return user is not None and user.email == ADMIN_EMAIL