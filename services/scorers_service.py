import requests

SCORERS_URL = (
    "https://raw.githubusercontent.com/"
    "rezarahiminia/worldcup2026/main/"
    "football.matches.json"
)


def limpiar_goleadores(texto):

    if not texto:
        return []

    texto = str(texto).strip()

    if texto.lower() == "null":
        return []

    goleadores = []

    for parte in texto.split(","):

        nombre = parte.split("(")[0].strip()

        if nombre:
            goleadores.append(nombre)

    return goleadores


def obtener_goleadores(partido_id):

    try:

        response = requests.get(
            SCORERS_URL,
            timeout=30
        )

        data = response.json()

        for partido in data:

            if str(partido["id"]) == str(partido_id):

                home_scorers = limpiar_goleadores(
                    partido.get(
                        "home_scorers",
                        ""
                    )
                )

                away_scorers = limpiar_goleadores(
                    partido.get(
                        "away_scorers",
                        ""
                    )
                )

                todos = (
                    home_scorers
                    +
                    away_scorers
                )

                return ";".join(todos)

        return ""

    except Exception as e:

        print(
            f"Error obteniendo goleadores: {e}"
        )

        return ""