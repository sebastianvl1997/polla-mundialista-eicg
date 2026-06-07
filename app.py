import streamlit as st
from services.auth import supabase
from database.sheets import connect
from database.users import (
    get_user_by_email,
    create_user,
    update_last_activity
)

from datetime import datetime, timedelta

supabase.auth.get_session()

if "session" in st.session_state:
    session = st.session_state["session"]

    # verificar expiración por inactividad
    last = st.session_state.get("last_activity")

    if last:
        if datetime.now() - last > timedelta(minutes=30):
            st.session_state.clear()
            st.warning("Sesión expirada por inactividad")
            st.stop()

    st.session_state["last_activity"] = datetime.now()

st.title("Login")

# --------------------
# CALLBACK OAUTH
# --------------------
params = st.query_params

if (
    "code" in params
    and "user" not in st.session_state
):

    try:

        
        session = supabase.auth.exchange_code_for_session({
            "auth_code": params["code"]
        })

        st.session_state["session"] = session
        st.session_state["user"] = session.user
        st.session_state["last_activity"] = datetime.now()

        # -------------------------
        # Guardar en Google Sheets
        # -------------------------

        spreadsheet = connect()

        usuarios_sheet = spreadsheet.worksheet(
            "Usuarios"
        )

        email = session.user.email

        nombre = session.user.user_metadata.get(
            "full_name",
            email
        )

        user_sheet = get_user_by_email(
            usuarios_sheet,
            email
        )

        if not user_sheet:

            create_user(
                usuarios_sheet,
                nombre,
                email
            )

        else:

            update_last_activity(
                usuarios_sheet,
                email
            )

    except Exception:
        pass

    st.query_params.clear()
    st.rerun()

# --------------------
# USER
# --------------------
user = st.session_state.get("user")

if user:

    st.success(
        f"Logueado: {user.email}"
    )

    st.stop()

# --------------------
# LOGIN
# --------------------
if st.button("Login con Google"):

    data = supabase.auth.sign_in_with_oauth({
        "provider": "google",
        "options": {
            "redirect_to":
            "https://polla-mundialista-eicg-svl.streamlit.app"
        }
    })

    st.markdown(
        f"[Continuar con Google]({data.url})"
    )
