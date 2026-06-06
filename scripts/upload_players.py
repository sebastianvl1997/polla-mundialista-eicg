import re
import pdfplumber
import pandas as pd

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

            # Selección
            team_match = re.match(
                r"^(.*?) \(([A-Z]{3})\)$",
                line
            )

            if team_match:
                current_team = team_match.group(1).strip()
                continue

            if current_team is None:
                continue

            # Jugadores
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

                # Eliminar duplicación inicial
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

print(df.head(30))
print()
print("TOTAL:", len(df))

df.to_csv(
    "jugadores.csv",
    index=False,
    encoding="utf-8-sig"
)

print("CSV generado: jugadores.csv")