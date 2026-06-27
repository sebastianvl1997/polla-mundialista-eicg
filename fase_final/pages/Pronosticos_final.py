from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
    
import streamlit as st
import pandas as pd

from database.sheets import connect
from services.fixture_service import get_group_stage_matches

# from services.permissions_service import (
#     puede_jugar_final
# )

# user = st.session_state.get("user")

# if not user:
#     st.stop()

# if not puede_jugar_final(user.email):

#     st.error(
#         "No estás inscrito para participar en la fase final, comunícate con el Administrador al 3053435734."
#     )

#     st.stop()

st.title("🔮 Pronósticos de los participantes")

spreadsheet = connect()

usuarios_sheet = spreadsheet.worksheet("Usuarios_Final")
pronosticos_sheet = spreadsheet.worksheet("Pronosticos_Final")

usuarios_df = pd.DataFrame(
    usuarios_sheet.get_all_records()
)

pronosticos_df = pd.DataFrame(
    pronosticos_sheet.get_all_records()
)

if pronosticos_df.empty:
    pronosticos_df = pd.DataFrame(
        columns=[
            "user_id",
            "partido_id",
            "goles_local",
            "goles_visitante",
            "goleador",
            "ultima_modificacion"
        ]
    )

fixture_df = get_group_stage_matches()

# --------------------------
# Selector de partido
# --------------------------

partidos = {
    row["MatchNumber"]:
    f"{row['HomeTeam']} vs {row['AwayTeam']}"
    for _, row in fixture_df.iterrows()
}

partido_id = st.selectbox(
    "⚽ Selecciona un partido",
    options=list(partidos.keys()),
    format_func=lambda x: partidos[x]
)

# --------------------------
# Información del partido
# --------------------------

partido = fixture_df[
    fixture_df["MatchNumber"] == partido_id
].iloc[0]

st.subheader(
    f"{partido['HomeTeam']} vs {partido['AwayTeam']}"
)

# --------------------------
# Pronósticos del partido
# --------------------------

pronosticos_partido = pronosticos_df[
    pronosticos_df["partido_id"].astype(str)
    ==
    str(partido_id)
]

if pronosticos_partido.empty:

    st.info(
        "Todavía no hay pronósticos para este partido."
    )

else:

    # unir con usuarios
    tabla = pronosticos_partido.merge(
        usuarios_df[
            ["user_id", "nombre"]
        ],
        on="user_id",
        how="left"
    )

    tabla["Pronóstico"] = (
        tabla["goles_local"].astype(str)
        + " - "
        + tabla["goles_visitante"].astype(str)
    )

    tabla["Goleador"] = tabla["goleador"].fillna("")

    tabla = tabla[
        [
            "nombre",
            "Pronóstico",
            "Goleador"
        ]
    ]

    tabla.columns = [
        "Participante",
        "Pronóstico",
        "Goleador"
    ]

    tabla = tabla.sort_values(
        by="Participante"
    )

    st.dataframe(
        tabla,
        use_container_width=True,
        hide_index=True
    )