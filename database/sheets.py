import os
import gspread
import streamlit as st

SPREADSHEET_ID = "1ny7DoyHOd4MipYtBWew9EoQYiXFgvgyaerGRZVhH3UQ"

@st.cache_resource
def connect():

    if os.path.exists(
        "credentials/service_account.json"
    ):

        gc = gspread.service_account(
            filename="credentials/service_account.json"
        )

    else:

        gc = gspread.service_account_from_dict(
            st.secrets["gcp_service_account"]
        )

    spreadsheet = gc.open_by_key(
        SPREADSHEET_ID
    )

    return spreadsheet