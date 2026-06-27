from database.sheets import connect
from services.fixture_service import get_all_matches
from services.results_service import actualizar_resultado
from services.ranking_service import (
    actualizar_ranking
)
import pandas as pd


def sincronizar_resultados():

    spreadsheet = connect()

    usuarios_sheet = spreadsheet.worksheet("Usuarios_Final")
    pronosticos_sheet = spreadsheet.worksheet("Pronosticos_Final")
    resultados_sheet = spreadsheet.worksheet("Resultados")
    ranking_sheet = spreadsheet.worksheet("Ranking_Final")
    
    resultados = resultados_sheet.get_all_records()

    df = get_all_matches()

    for _, row in df.iterrows():
   

        hg = row.get("HomeTeamScore")
        ag = row.get("AwayTeamScore")

        if pd.isna(hg) or pd.isna(ag):
            continue

        print("Partido", row["MatchNumber"])

        actualizar_resultado(
            resultados_sheet,
            ranking_sheet,
            usuarios_sheet,
            pronosticos_sheet,
            resultados,   
            row["MatchNumber"],
            int(hg),
            int(ag)
        )
        
    actualizar_ranking(
        usuarios_sheet,
        pronosticos_sheet,
        resultados_sheet,
        ranking_sheet
    )