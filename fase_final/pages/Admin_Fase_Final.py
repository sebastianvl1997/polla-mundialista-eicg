from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import streamlit as st
from auth_utils import is_admin, get_user
from services.sync_results_service_final import sincronizar_resultados


user = get_user()

if not user:
    st.error("Debes iniciar sesión")
    st.stop()

if not is_admin():
    st.error("Espacio destinado únicamente para administradores")
    st.stop()

st.title("Panel de Administración")
st.write("Contenido sensible aquí")

st.title("🔒 Administración")

st.warning("Panel reservado para administradores.")

import streamlit as st

from database.sheets import connect

from services.results_service import (
    actualizar_resultado
)

from services.fase_final_service import (
    cerrar_fase_grupos
)

spreadsheet = connect()

usuarios_sheet = spreadsheet.worksheet(
    "Usuarios"
)

pronosticos_sheet = spreadsheet.worksheet(
    "Pronosticos"
)

resultados_sheet = spreadsheet.worksheet(
    "Resultados"
)

ranking_sheet = spreadsheet.worksheet(
    "Ranking"
)

st.title("⚙️ Cargar resultados")

partido_id = st.number_input(
    "Partido",
    min_value=1,
    step=1
)

goles_local = st.number_input(
    "Goles local",
    min_value=0,
    step=1
)

goles_visitante = st.number_input(
    "Goles visitante",
    min_value=0,
    step=1
)

goleador = st.text_input(
    "Goleador"
)

if st.button(
    "Guardar resultado"
):

    actualizar_resultado(
        resultados_sheet,
        ranking_sheet,
        usuarios_sheet,
        pronosticos_sheet,
        partido_id,
        goles_local,
        goles_visitante,
        goleador
    )

    st.success(
        "Resultado actualizado y ranking recalculado"
    )


if st.button("Sincronizar resultados"):
    sincronizar_resultados()
    
    