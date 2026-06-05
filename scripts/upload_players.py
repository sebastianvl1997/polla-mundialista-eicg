import sys
from pathlib import Path

sys.path.append(
    str(Path(__file__).resolve().parents[1])
)

import pandas as pd

from database.sheets import connect

spreadsheet = connect()

sheet = spreadsheet.worksheet("Jugadores")

df = pd.read_csv(
    "jugadores.csv",
    encoding="utf-8-sig"
)

sheet.clear()

sheet.append_row([
    "equipo",
    "jugador"
])

rows = df.values.tolist()

BATCH_SIZE = 500

for i in range(0, len(rows), BATCH_SIZE):

    batch = rows[i:i + BATCH_SIZE]

    sheet.append_rows(batch)

    print(
        f"Cargadas {min(i + BATCH_SIZE, len(rows))} filas"
    )

print("Finalizado")