import streamlit as st
import pandas as pd
from services.sync_results_service import (
    sincronizar_resultados
)

from database.sheets import connect

st.title("🏆 Ranking General")

sincronizar_resultados()

spreadsheet = connect()

ranking_sheet = spreadsheet.worksheet(
    "Ranking"
)

resultados_sheet = spreadsheet.worksheet(
    "Resultados"
)

ranking = ranking_sheet.get_all_records()

if not ranking:

    st.info(
        "Aún no hay puntajes calculados."
    )

    st.stop()

df = pd.DataFrame(ranking)

# Posición

df.insert(
    0,
    "Posición",
    range(1, len(df) + 1)
)

# Renombrar columnas

df = df.rename(
    columns={
        "nombre": "Participante",
        "puntos": "Puntos",
        "exactos": "Exactos",
        "resultados": "Resultados",
        "goleadores": "Goleadores"
    }
)

# Ocultar user_id

if "user_id" in df.columns:
    df = df.drop(
        columns=["user_id"]
    )

st.table(df)

st.caption(
    "Criterio de desempate: Exactos → Resultados → Goleadores."
)

# ----------------------------------------
# Última actualización
# ----------------------------------------

resultados = resultados_sheet.get_all_records()

fechas = [
    str(r["ultima_actualizacion"]).strip()
    for r in resultados
    if str(r["ultima_actualizacion"]).strip()
]

if fechas:

    ultima_actualizacion = max(fechas)

    st.caption(
        f"Nota: Ranking actualizado con resultados oficiales al {ultima_actualizacion}."
    )