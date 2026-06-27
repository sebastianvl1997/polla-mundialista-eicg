# -*- coding: utf-8 -*-
"""
Created on Wed Jun 17 15:59:30 2026

@author: Sebastian
"""

import streamlit as st
import pandas as pd

from database.sheets import connect
from services.fixture_service import get_all_matches
from services.scoring import evaluar_pronostico





st.title("📋 Pronósticos de los participantes (FASE FINAL)")

spreadsheet = connect()

usuarios_sheet = spreadsheet.worksheet("Participantes_Final")
pronosticos_sheet = spreadsheet.worksheet("Pronosticos_Final")
resultados_sheet = spreadsheet.worksheet("Resultados")

usuarios = usuarios_sheet.get_all_records()
pronosticos = pronosticos_sheet.get_all_records()
resultados = resultados_sheet.get_all_records()

participantes = sorted([u["nombre"] for u in usuarios])

participante = st.selectbox(
    "Participante",
    participantes
)

usuario = next(
    u for u in usuarios
    if u["nombre"] == participante
)

user_id = str(usuario["user_id"])

pronosticos_usuario = [
    p for p in pronosticos
    if str(p["user_id"]) == user_id
]

resultados_map = {
    str(r["partido_id"]): r
    for r in resultados
}

fixture = get_all_matches()

filas = []

total_puntos = 0
total_exactos = 0
total_resultados = 0
total_goleadores = 0

for _, match in fixture.iterrows():

    partido_id = str(match["MatchNumber"])

    pron = next(
        (
            p for p in pronosticos_usuario
            if str(p["partido_id"]) == partido_id
        ),
        None
    )

    resultado = resultados_map.get(partido_id)

    puntos = ""
    exacto = ""
    resultado_ok = ""
    goleador_ok = ""

    if pron and resultado:

        evaluacion = evaluar_pronostico(
            pron,
            resultado
        )

        puntos = evaluacion["puntos"]
        exacto = "✓" if evaluacion["exacto"] else ""
        resultado_ok = "✓" if evaluacion["resultado"] else ""
        goleador_ok = "✓" if evaluacion["goleador"] else ""

        total_puntos += evaluacion["puntos"]
        total_exactos += int(evaluacion["exacto"])
        total_resultados += int(evaluacion["resultado"])
        total_goleadores += int(evaluacion["goleador"])

    filas.append({
        "Partido":
            f"{match['HomeTeam']} vs {match['AwayTeam']}",

        "Pronóstico":
            ""
            if not pron
            else
            f"{pron['goles_local']}-{pron['goles_visitante']}",

        "Goleador pronóstico":
            ""
            if not pron
            else
            pron["goleador"],

        "Resultado real":
            ""
            if not resultado
            else
            f"{resultado['goles_local']}-{resultado['goles_visitante']}",

        "Goleadores reales":
            ""
            if not resultado
            else
            resultado["goleador_final"],

        "Pts":
            puntos,

        "Exacto":
            exacto,

        "Resultado":
            resultado_ok,

        "Goleador":
            goleador_ok
    })

filas.append({
    "Partido": "TOTAL",
    "Pronóstico": "",
    "Goleador pronóstico": "",
    "Resultado real": "",
    "Goleadores reales": "",
    "Pts": total_puntos,
    "Exacto": total_exactos,
    "Resultado": total_resultados,
    "Goleador": total_goleadores
})

df = pd.DataFrame(filas)

st.dataframe(
    df,
    use_container_width=True,
    hide_index=True
)