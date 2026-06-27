# -*- coding: utf-8 -*-
"""
Created on Thu Jun 25 14:13:30 2026

@author: Sebastian
"""

from database.sheets import connect

def es_admin(email):

    return (
        email.lower()
        ==
        "sebastianvl1997@gmail.com"
    )

def puede_jugar_final(email):

    spreadsheet = connect()

    sheet = spreadsheet.worksheet(
        "Participantes_Final"
    )

    participantes = sheet.col_values(1)

    return (
        email.lower()
        in
        [x.lower() for x in participantes]
    )