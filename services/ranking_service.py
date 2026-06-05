from services.scoring import calcular_ranking


def actualizar_ranking(
    usuarios_sheet,
    pronosticos_sheet,
    resultados_sheet,
    ranking_sheet
):

    usuarios = usuarios_sheet.get_all_records()

    pronosticos = pronosticos_sheet.get_all_records()

    resultados = resultados_sheet.get_all_records()

    ranking = calcular_ranking(
        pronosticos,
        resultados
    )

    nombres = {
        str(u["user_id"]): u["nombre"]
        for u in usuarios
    }

    ranking_sheet.clear()

    ranking_sheet.append_row([
        "user_id",
        "nombre",
        "puntos",
        "exactos",
        "resultados",
        "goleadores"
    ])

    rows = []

    for fila in ranking:

        user_id = str(fila["user_id"])

        rows.append([
            user_id,
            nombres.get(user_id, ""),
            fila["puntos"],
            fila["exactos"],
            fila["resultados"],
            fila["goleadores"]
        ])

    if rows:
        ranking_sheet.append_rows(rows)