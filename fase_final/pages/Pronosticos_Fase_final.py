from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import streamlit as st
import pandas as pd

from database.sheets import connect
from services.fixture_service import (
    get_knockout_matches,
    get_flag_url
)

def to_colombia_time(date_utc):

    if not date_utc or date_utc == "N/A":
        return "N/A"

    return (
        pd.to_datetime(date_utc, utc=True)
        .tz_convert("America/Bogota")
        .strftime("%Y-%m-%d %H:%M")
    )

st.title("🔮 Pronósticos de los participantes")

spreadsheet = connect()

usuarios_sheet = spreadsheet.worksheet("Usuarios_Final")
pronosticos_sheet = spreadsheet.worksheet("Pronosticos_Final")
campeon_sheet = spreadsheet.worksheet("Campeon_Final")

usuarios_df = pd.DataFrame(usuarios_sheet.get_all_records())
pronosticos_df = pd.DataFrame(pronosticos_sheet.get_all_records())
campeon_df = pd.DataFrame(campeon_sheet.get_all_records())

if pronosticos_df.empty:
    pronosticos_df = pd.DataFrame(columns=[
        "user_id",
        "partido_id",
        "goles_local",
        "goles_visitante",
        "goleador",
        "ultima_modificacion"
    ])

# --------------------------
# FIXTURE FASE FINAL
# --------------------------
df = get_knockout_matches()
df = df[df["RoundNumber"] >= 4]

rondas = {
    4: "Dieciseisavos",
    5: "Octavos",
    6: "Cuartos",
    7: "Semifinales",
    8: "Final y 3.er puesto"
}

# --------------------------
# TABS POR RONDA
# --------------------------
rondas_existentes = sorted(df["RoundNumber"].unique())

tabs = st.tabs(
    [rondas[r] for r in rondas_existentes] +
    ["🏆 Campeón"]
)

for tab, ronda in zip(tabs[:-1], rondas_existentes):

    with tab:

        df_ronda = df[df["RoundNumber"] == ronda]

        for _, partido in df_ronda.iterrows():

            st.markdown("###")

            with st.container(border=True):

                partido_id = partido["MatchNumber"]

                # --------------------------
                # HEADER PARTIDO
                # --------------------------
                col_info = st.columns([1, 2, 2, 2])

                with col_info[0]:
                    st.markdown(f"**⚽ Partido {partido_id}**")
                
                with col_info[1]:
                    st.markdown(f"**🏆 {rondas[ronda]}**")
                
                with col_info[2]:
                    st.markdown(
                        f"🕒 {to_colombia_time(partido.get('DateUtc'))}"
                    )
                
                with col_info[3]:
                    st.markdown(
                        f"🏟️ {partido.get('Location', 'N/A')}"
                    )

                st.divider()

                # --------------------------
                # MATCH DISPLAY (FLAGS)
                # --------------------------
                col1, col2, col3 = st.columns([3, 1, 3])

                with col1:
                    c1, c2 = st.columns([1, 4])
                    with c1:
                        st.image(get_flag_url(partido["HomeTeam"]), width=45)
                    with c2:
                        st.markdown(f"### {partido['HomeTeam']}")

                with col2:
                    st.markdown("## VS")

                with col3:
                    c1, c2 = st.columns([1, 4])
                    with c1:
                        st.image(get_flag_url(partido["AwayTeam"]), width=45)
                    with c2:
                        st.markdown(f"### {partido['AwayTeam']}")

                # --------------------------
                # PRONÓSTICOS
                # --------------------------
                pronosticos_partido = pronosticos_df[
                    pronosticos_df["partido_id"].astype(str)
                    == str(partido_id)
                ]

                if pronosticos_partido.empty:
                    st.info("Todavía no hay pronósticos para este partido.")
                    continue

                tabla = pronosticos_partido.merge(
                    usuarios_df[["user_id", "nombre"]],
                    on="user_id",
                    how="left"
                )

                tabla["Pronóstico"] = (
                    tabla["goles_local"].astype(str)
                    + " - "
                    + tabla["goles_visitante"].astype(str)
                )

                tabla["Goleador"] = tabla["goleador"].fillna("")

                tabla = tabla[[
                    "nombre",
                    "Pronóstico",
                    "Goleador"
                ]].rename(columns={
                    "nombre": "Participante"
                }).sort_values("Participante")

                st.dataframe(
                    tabla,
                    use_container_width=True,
                    hide_index=True
                )
                
with tabs[-1]:

    st.subheader("🏆 Pronóstico de campeón")

    if campeon_df.empty:

        st.info("Nadie ha seleccionado un campeón todavía.")

    else:

        tabla = campeon_df.merge(
            usuarios_df[["user_id", "nombre"]],
            on="user_id",
            how="left"
        )

        tabla = tabla.rename(columns={
            "nombre": "Participante",
            "campeon": "Campeón"
        })

        tabla = tabla[[
            "Participante",
            "Campeón"
        ]].sort_values("Participante")

        st.dataframe(
            tabla,
            hide_index=True,
            use_container_width=True
        )