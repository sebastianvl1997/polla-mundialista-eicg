# -*- coding: utf-8 -*-
"""
Created on Thu Jun 25 14:06:28 2026

@author: Sebastian
"""

from database.sheets import connect

def obtener_etapa():

    spreadsheet = connect()

    sheet = spreadsheet.worksheet(
        "Etapa"
    )

    datos = sheet.get_all_records()

    for fila in datos:

        if fila["clave"] == "etapa_actual":

            return fila["valor"]

    return "GRUPOS"