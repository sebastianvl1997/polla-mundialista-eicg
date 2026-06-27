from datetime import datetime


def get_prediction(records, user_id, partido_id):


    for row in records:

        if (
            str(row["user_id"]) == str(user_id)
            and
            str(row["partido_id"]) == str(partido_id)
        ):
            return row

    return None


def save_prediction(
    sheet,
    user_id,
    partido_id,
    goles_local,
    goles_visitante,
    goleador=""
):

    records = sheet.get_all_records()
    
    prediction = get_prediction(
        records,
        user_id,
        partido_id
    )

    now = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    # actualizar

    if prediction:

        records = sheet.get_all_records()

        for idx, row in enumerate(records, start=2):

            if (
                str(row["user_id"]) == str(user_id)
                and
                str(row["partido_id"]) == str(partido_id)
            ):

                sheet.update(
                    f"C{idx}:F{idx}",
                    [[
                        goles_local,
                        goles_visitante,
                        goleador,
                        now
                    ]]
                )

                return

    # insertar nuevo

    sheet.append_row([
        user_id,
        partido_id,
        goles_local,
        goles_visitante,
        goleador,
        now
    ])
    
    


from zoneinfo import ZoneInfo


def get_champion(sheet, user_id):

    registros = sheet.get_all_records()

    for row in registros:

        if str(row["user_id"]) == str(user_id):
            return row

    return None




def save_champion(
    sheet,
    user_id,
    campeon
):

    now = datetime.now(
        ZoneInfo("America/Bogota")
    ).strftime("%Y-%m-%d %H:%M:%S")

    registros = sheet.get_all_records()

    for idx, row in enumerate(
        registros,
        start=2
    ):

        if str(row["user_id"]) == str(user_id):

            sheet.update(
                f"A{idx}:C{idx}",
                [[
                    user_id,
                    campeon,
                    now
                ]]
            )

            return

    sheet.append_row([
        user_id,
        campeon,
        now
    ])