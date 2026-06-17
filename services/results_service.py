from datetime import datetime
from zoneinfo import ZoneInfo


from services.ranking_service import (
    actualizar_ranking
)

from services.scorers_service import (
    obtener_goleadores
)

def actualizar_resultado(
    resultados_sheet,
    ranking_sheet,
    usuarios_sheet,
    pronosticos_sheet,
    resultados,
    partido_id,
    goles_local,
    goles_visitante,
):

    print("Leyendo hoja Resultados...")

    # resultados = (
    #     resultados_sheet.get_all_records()
    # )
    # print("Lectura completada")


    now = datetime.now(
        ZoneInfo("America/Bogota")
    ).strftime(
        "%Y-%m-%d %H:%M:%S"
    )
    
    goleador_auto = obtener_goleadores(
    partido_id
)

    actualizado = False

    for idx, row in enumerate(
        resultados,
        start=2
    ):

        if str(row["partido_id"]) == str(partido_id):

            goleador_manual = str(
                row.get("goleador_manual", "")
            ).strip()

            goleador_final = (
                goleador_manual
                if goleador_manual
                else goleador_auto
            )

            resultados_sheet.update(
                f"B{idx}:G{idx}",
                [[
                    goles_local,
                    goles_visitante,
                    goleador_auto,
                    goleador_manual,
                    goleador_final,
                    now
                ]]
            )

            actualizado = True
            break

    if not actualizado:

        goleador_final = goleador_auto

        resultados_sheet.append_row([
            partido_id,
            goles_local,
            goles_visitante,
            goleador_auto,
            "",
            goleador_final,
            now
        ])

    # recalcular ranking

    actualizar_ranking(
        usuarios_sheet,
        pronosticos_sheet,
        resultados_sheet,
        ranking_sheet
    )