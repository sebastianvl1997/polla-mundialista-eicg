from database.sheets import connect
from services.fixture_service import get_all_matches
from services.results_service import actualizar_resultado


def sincronizar_resultados():

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

    df = get_all_matches()

    for _, row in df.iterrows():

        hg = row.get("HomeGoals")
        ag = row.get("AwayGoals")

        if hg == "" or ag == "":
            continue

        actualizar_resultado(
            resultados_sheet,
            ranking_sheet,
            usuarios_sheet,
            pronosticos_sheet,
            row["MatchNumber"],
            int(hg),
            int(ag)
        )