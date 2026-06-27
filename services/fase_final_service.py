# -*- coding: utf-8 -*-
"""
Created on Thu Jun 25 15:24:16 2026

@author: Sebastian
"""

from database.sheets import connect


def cerrar_fase_grupos():

    spreadsheet = connect()

    ranking_sheet = spreadsheet.worksheet(
        "Ranking"
    )

    posiciones_sheet = spreadsheet.worksheet(
        "Posiciones_Finales_Grupos"
    )

    configuracion_sheet = spreadsheet.worksheet(
        "Etapa"
    )

    ranking_final_sheet = spreadsheet.worksheet(
        "Ranking_Final"
    )

    # copiar ranking actual

    ranking_actual = (
        ranking_sheet.get_all_values()
    )

    posiciones_sheet.clear()

    if ranking_actual:
        posiciones_sheet.update(
            "A1",
            ranking_actual
        )

    # limpiar ranking final

    ranking_final_sheet.clear()

    ranking_final_sheet.append_row([
        "user_id",
        "nombre",
        "puntos",
        "exactos",
        "resultados",
        "goleadores"
    ])

    # cambiar etapa

    configuracion_sheet.update(
        "B2",
        [["FINAL"]]
    )