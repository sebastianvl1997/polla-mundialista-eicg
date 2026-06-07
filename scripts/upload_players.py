import sys
import os

sys.path.append(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)

from database.sheets import connect
import re
import pdfplumber
import pandas as pd

from database.sheets import connect

PDF_FILE = r"data/SquadLists-English.pdf"

players = []

# Traducción de posiciones
posiciones = {
    "GK": "Arquero",
    "DF": "Defensa",
    "MF": "Mediocampista",
    "FW": "Delantero"
}

with pdfplumber.open(PDF_FILE) as pdf:

    current_team = None

    for page in pdf.pages:

        text = page.extract_text()

        if not text:
            continue

        lines = text.split("\n")

        for line in lines:

            team_match = re.match(
                r"^(.*?) \(([A-Z]{3})\)$",
                line
            )

            if team_match:
                current_team = team_match.group(1).strip()
                continue

            if current_team is None:
                continue

            m = re.match(
                r"^\d+\s+(GK|DF|MF|FW)\s+([A-ZÀ-ÖØ-Ý' -]+)\s+(.+?)\s+\d{2}/\d{2}/\d{4}",
                line
            )

            if m:

                codigo_posicion = m.group(1)

                apellido = m.group(2).title().strip()

                resto = m.group(3).strip()

                nombre = resto.split()[0]

                jugador = f"{nombre} {apellido}"

                jugador_parts = jugador.split()

                if (
                    len(jugador_parts) >= 2
                    and jugador_parts[0].lower()
                    == jugador_parts[1].lower()
                ):
                    jugador = " ".join(jugador_parts[1:])

                players.append(
                    [
                        current_team,
                        jugador,
                        posiciones[codigo_posicion]
                    ]
                )

df = pd.DataFrame(
    players,
    columns=[
        "equipo",
        "jugador",
        "posicion"
    ]
)

print(df.head())
print()
print("TOTAL:", len(df))

# -------------------------
# Subir a Google Sheets
# -------------------------

spreadsheet = connect()

jugadores_sheet = spreadsheet.worksheet(
    "Jugadores"
)

jugadores_sheet.clear()

jugadores_sheet.update(
    [df.columns.values.tolist()]
    + df.values.tolist()
)

print("Hoja Jugadores actualizada.")