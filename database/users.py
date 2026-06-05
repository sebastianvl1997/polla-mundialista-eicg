import uuid
from datetime import datetime

def get_user_by_email(sheet, email):

    records = sheet.get_all_records()

    for row in records:
        if row["email"].lower() == email.lower():
            return row

    return None


def create_user(sheet, nombre, email):

    user_id = str(uuid.uuid4())

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    sheet.append_row([
        user_id,
        email,
        nombre,
        now,
        "ACTIVO",
        now,
        0
    ])

    return user_id

from datetime import datetime

def update_last_activity(sheet, email):

    records = sheet.get_all_records()

    for idx, row in enumerate(records, start=2):

        if row["email"].lower() == email.lower():

            now = datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )

            # columna F = ultima_actividad
            sheet.update_cell(idx, 6, now)

            return True

    return False