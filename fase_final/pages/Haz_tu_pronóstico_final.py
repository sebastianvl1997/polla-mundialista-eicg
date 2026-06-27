from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
    
import streamlit as st
import pandas as pd
from database.sheets import connect
from datetime import datetime, timedelta
from database.pronosticos import (
    save_prediction,
    get_prediction
)

from database.users import get_user_by_email

from services.permissions_service import (
    puede_jugar_final
)



st.title("⚽ Calendario")

st.info("Aquí aparecerán los 32 partidos de las fases finales (knockout).")

user = st.session_state.get("user")

if not user:
    st.warning("Debes iniciar sesión")
    st.stop()
    
if not puede_jugar_final(user.email):

    st.error(
        "No estás inscrito para participar en la fase final, comunícate con el Administrador al 3053435734."
    )

    st.stop()

@st.cache_resource
def get_spreadsheet():
    return connect()

spreadsheet = get_spreadsheet()

@st.cache_resource
def get_sheets(_spreadsheet):
    return (
        _spreadsheet.worksheet("Usuarios_Final"),
        _spreadsheet.worksheet("Pronosticos_Final"),
        _spreadsheet.worksheet("Jugadores"),
    )

usuarios_sheet, pronosticos_sheet, jugadores_sheet = get_sheets(spreadsheet)

@st.cache_data(ttl=300)
def load_jugadores(_sheet):
    return pd.DataFrame(_sheet.get_all_records())

jugadores_df = load_jugadores(jugadores_sheet)

email = user.email

usuario = get_user_by_email(
    usuarios_sheet,
    email
)

user_id = usuario["user_id"]



from services.fixture_service import get_flag_url
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


df = get_knockout_matches()


@st.cache_data(ttl=120)
def load_predicciones(_sheet):
    return _sheet.get_all_records()
predicciones = load_predicciones(pronosticos_sheet)

@st.cache_data(ttl=120)
def get_user_predictions(_sheet, user_id):
    data = _sheet.get_all_records()
    return [
        p for p in data
        if str(p.get("user_id")) == str(user_id)
    ]

predicciones_usuario = get_user_predictions(pronosticos_sheet, user_id)

orden = [
    "Round of 32",
    "Round of 16",
    "Quarter-finals",
    "Semi-finals",
    "Third-place play-off",
    "Final"
]

nombres = {
    "Round of 32": "Dieciseisavos de final",
    "Round of 16": "Octavos de final",
    "Quarter-finals": "Cuartos de final",
    "Semi-finals": "Semifinales",
    "Third-place play-off": "Tercer puesto",
    "Final": "Final"
}

rondas_disponibles = [
    r for r in orden
    if r in df["RoundName"].unique()
]

ronda = st.selectbox(
    "🏆 Selecciona la fase",
    rondas_disponibles,
    format_func=lambda x: nombres[x]
)

df = df[
    df["RoundName"] == ronda
]

for _, row in df.iterrows():

    st.markdown("###")

    # HEADER: hora + estadio + grupo
    
    with st.container(border=True):
    
        col_info = st.columns(3)
    
        with col_info[0]:
            st.write(f"🕒 {to_colombia_time(row.get('DateUtc'))}")
    
        with col_info[1]:
            st.write(f"🏟️ {row.get('Location', 'N/A')}")
    
        with col_info[2]:
            st.write(f"🏆 {nombres.get(row["RoundName"], row["RoundName"])}")
    
        st.divider()
    
        # PARTIDO
        col1, col2, col3 = st.columns([3, 1, 3])
    
        with col1:
            c1, c2 = st.columns([1, 4])
            with c1:
                st.image(get_flag_url(row["HomeTeam"]), width=50)
            with c2:
                st.markdown(
                    f"### {row['HomeTeam']}"
                )
    
        with col2:
            st.markdown("## VS")
    
            # resultado si existe
            hg = row.get("HomeGoals", "")
            ag = row.get("AwayGoals", "")
            if hg != "" and ag != "":
                st.caption(f"{hg} - {ag}")
    
        with col3:
            c1, c2 = st.columns([1, 4])
            with c1:
                st.image(get_flag_url(row["AwayTeam"]), width=50)
            with c2:
                st.markdown(
                    f"### {row['AwayTeam']}"
                )
    
        partido_id = row["MatchNumber"]
        

        


        fecha_partido = pd.to_datetime(
            row["DateUtc"],
            utc=True
        ).tz_convert("America/Bogota")
        
        hora_cierre = fecha_partido - timedelta(
            minutes=10
        )
        
        partido_bloqueado = (
            datetime.now(fecha_partido.tzinfo)
            >=
            hora_cierre
        )
        
        prediction = next(
            (
                p for p in predicciones_usuario
                if str(p["partido_id"]) == str(partido_id)
            ),
            None
        )
                
        
        if prediction:
        
            default_local = int(
                prediction["goles_local"]
            )
        
            default_visitante = int(
                prediction["goles_visitante"]
            )
            
            default_goleador = str(
                prediction.get("goleador", "")
            )
        
        else:
        
            default_local = 0
            default_visitante = 0
            default_goleador = ""
        
        
        st.markdown("##### 🎯 Tu pronóstico")
        
        col_local, col_vs, col_visitante = st.columns([3, 1, 3])
        
        with col_local:
            st.markdown(f"**{row['HomeTeam']}**")
            goles_local = st.number_input(
                label="",
                min_value=0,
                max_value=20,
                value=default_local,
                key=f"hl_{partido_id}",
                disabled=partido_bloqueado
            )
        
        with col_vs:
            st.markdown(
                "<div style='text-align:center; font-size:22px; font-weight:bold;'>VS</div>",
                unsafe_allow_html=True
            )
        
        with col_visitante:
            st.markdown(f"**{row['AwayTeam']}**")
            goles_visitante = st.number_input(
                label="",
                min_value=0,
                max_value=20,
                value=default_visitante,
                key=f"av_{partido_id}",
                disabled=partido_bloqueado
            )
            
    equipo_local = row["HomeTeam"]
    equipo_visitante = row["AwayTeam"]
    
    jugadores_partido = jugadores_df[
        jugadores_df["equipo"].isin(
            [equipo_local, equipo_visitante]
        )
    ]
    
    opciones_goleador = {
        f"{r['jugador']} ({r['equipo']} - {r['posicion']})":
        r["jugador"]
        for _, r in jugadores_partido.iterrows()
    }
    
    lista_display = [""] + sorted(
        opciones_goleador.keys()
    )
    
    indice_default = 0
    
    for i, texto in enumerate(lista_display):
        if opciones_goleador.get(texto, "") == default_goleador:
            indice_default = i
            break
    
    goleador_display = st.selectbox(
        "🎯 Hace gol en el partido",
        options=lista_display,
        index=indice_default,
        key=f"scorer_{partido_id}",
        disabled=partido_bloqueado
    )
    
    goleador = opciones_goleador.get(
        goleador_display,
        ""
    )

    if not partido_bloqueado:
        if st.button(
            "Guardar pronóstico",
            key=f"save_{partido_id}",
            disabled=partido_bloqueado
        ):
            with st.spinner("Guardando..."):
                save_prediction(
                    pronosticos_sheet,
                    user_id,
                    partido_id,
                    goles_local,
                    goles_visitante,
                    goleador
                )
        
            st.success("Pronóstico guardado")
            
    
        
    else:
        st.info("🔒 Pronóstico cerrado")

    st.divider()