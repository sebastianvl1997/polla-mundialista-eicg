import streamlit as st
import pandas as pd
from database.sheets import connect
from datetime import datetime
from database.pronosticos import (
    save_prediction,
    get_prediction
)

from database.users import get_user_by_email

st.title("⚽ Calendario")

st.info("Aquí aparecerán los 72 partidos de la fase de grupos.")

user = st.session_state.get("user")

if not user:
    st.warning("Debes iniciar sesión")
    st.stop()

spreadsheet = connect()

usuarios_sheet = spreadsheet.worksheet(
    "Usuarios"
)

pronosticos_sheet = spreadsheet.worksheet(
    "Pronosticos"
)

jugadores_sheet = spreadsheet.worksheet(
    "Jugadores"
)

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
    get_group_stage_matches,
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


df = get_group_stage_matches()


@st.cache_data(ttl=120)
def load_predicciones(_sheet):
    return _sheet.get_all_records()
predicciones = load_predicciones(pronosticos_sheet)

predicciones_usuario = [
    p for p in predicciones
    if str(p["user_id"]) == str(user_id)
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
            st.write(f"🏆 {row.get('Group', row.get('Stage', 'N/A'))}")
    
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
        
        partido_bloqueado = (
            datetime.now(fecha_partido.tzinfo)
            >=
            fecha_partido
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
    
    lista_jugadores = sorted(
        jugadores_partido["jugador"]
        .dropna()
        .unique()
        .tolist()
    )
    
    opciones_goleador = [""] + lista_jugadores
    
    indice_default = 0
    
    if default_goleador in opciones_goleador:
        indice_default = opciones_goleador.index(
            default_goleador
        )
    
    goleador = st.selectbox(
        "🎯 Goleador del partido",
        options=opciones_goleador,
        index=indice_default,
        key=f"scorer_{partido_id}",
        disabled=partido_bloqueado
    )

    if not partido_bloqueado:
        if st.button(
            "Guardar pronóstico",
            key=f"save_{partido_id}"
        ):
        
            save_prediction(
                pronosticos_sheet,
                user_id,
                partido_id,
                goles_local,
                goles_visitante,
                goleador
            )
        
            st.success(
                "Pronóstico guardado"
            )
    
    else:
        st.info("🔒 Pronóstico cerrado")

    st.divider()